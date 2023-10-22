from flight_control.plant import PlantSimulation
import os
# Stop pygame spamming the console when imported
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
import random
import multiprocessing

ASSET_DIR = os.path.dirname(os.path.abspath(__file__)) + "/assets"

ACTUATOR_MAX = 10
MIN_DISTURB_START = 0.5
MAX_IMPULSE_START = 1.0

RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_OFFSET = 25
PIXEL_OFFSET_Y_0 = (SCREEN_HEIGHT + TEXT_OFFSET) / 2
HUD_HEIGHT = 500


def run_simulation(plant, controller=None, disturbance=None, run_time_s=15.0, frame_rate_hz=60, discretisation_method='zoh'):
    """Simulation of a plant with a closed loop controller.

    Parameters
    ----------
    plant : TransferFunction
        A continuous time transfer function that describes
        the behaviour of the plant.

    controller : a controller object, optional
        An object to provide control to the system. Must
        have an 'update' and a 'get_control' method defined.

    disturbance : a disturbance object, optional
        A disturbance object (see disturbances.py).

    run_time_s : float
        How long to run the simulation for, in seconds.

    frame_rate_hz : int
        The refresh rate of the screen and the rate at which
        the system is discretised. Default 60.

    discretisation_method : 'zoh' | 'bilinear' | 'euler'
        The discretisation method (default 'zoh') to use.
            'zoh': Zero-Order Hold
            'bilinear': Tustin's transformation
            'euler': Euler's method (a.k.a. Forward Difference)
            'backward_diff': Backward Difference

    Returns
    -------
    result : tuple containing the results of the simulation.
        The three elements of the tuple are arrays containing:

            * time
            * error signal
            * control signal
    """
    # Note(charlie): in order to prevent the pygame window from sometimes lingering in
    # the background--which seems to happen on some operating systems when running the
    # simulation from within a Jupyter notebook--we'll spawn an entirely separate
    # process to run the simulation in.

    # However, as an extra complication, a user-defined class that is *not*
    # defined within an importable file, such as when using iPython in a Jupyter
    # notebook, pickle-based serialisation will fail... So just run those in the
    # same process.
    if controller and '__main__' in str(type(controller)).split("\'")[1].split("\'")[0]:
        return _run_simulation_internal(plant, controller, disturbance, run_time_s, frame_rate_hz, discretisation_method)
    else:
        args = (plant, controller, disturbance, run_time_s, frame_rate_hz, discretisation_method)
        pool = multiprocessing.Pool(1)
        results = pool.starmap(_run_simulation_internal, [args])[0]
        pool.close()
        pool.join()
        return results

def _run_simulation_internal(plant, controller, disturbance, run_time_s, frame_rate_hz, discretisation_method):
    if not _validate_simulation(plant, controller, disturbance):
        print("Simulation is incorrectly configured, exiting early")
        return [], [], []

    # Simulation initialisation
    sample_period = 1/frame_rate_hz
    model = PlantSimulation(plant.num, plant.den, sample_period, discretisation_method)
    simulation_time = 0.0

    disturbance_start_time = random.random() * (MAX_IMPULSE_START - MIN_DISTURB_START) + \
            MIN_DISTURB_START
    if disturbance:
        disturbance.initialise(frame_rate_hz, disturbance_start_time)

    time_tseries = []
    error_tseries = []
    control_tseries = []

    # Pygame initialisation
    pygame.init()
    icon = pygame.image.load(f"{ASSET_DIR}/plane_icon.png")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(f"{ASSET_DIR}/RobotoMono-Regular.ttf", 14)
    crash_font = pygame.font.Font(
        f"{ASSET_DIR}/RobotoMono-Regular.ttf", 48)

    # Initial gain control loop
    quit_while_waiting = _wait_for_click(screen, clock, font)
    if quit_while_waiting:
        pygame.quit()
        return np.array([]), np.array([]), np.array([])

    pygame.mouse.set_pos((SCREEN_WIDTH / 2, PIXEL_OFFSET_Y_0))

    # Main simulation loop
    for _ in range(int(run_time_s * frame_rate_hz)):
        user_quit = _handle_event_queue()
        if user_quit:
            break
        clock.tick(frame_rate_hz)

        # Start frame
        u = 0.0 if not controller else controller.get_control()
        u = np.clip(u, -10, 10)
        time_tseries.append(simulation_time)
        error_tseries.append(0 - model.get_output())
        control_tseries.append(u)

        # Update model
        simulation_time += sample_period
        d = 0.0 if not disturbance else disturbance.get_disturbance(
            simulation_time)
        # Note(Charlie): Typically, we would add a disturbance and
        # the control together. However, to make error signals
        # positive (more intuitive for the students), we're going
        # to make sure disturbances always send the nose of the
        # plane down.
        input_to_model = u - d
        model.tick(input_to_model)
        model_output = model.get_output()
        if controller:
            controller.update(0 - model_output, simulation_time - time_tseries[-1])

        # Draw the screen and handle crashes
        screen.fill(BLACK)
        crashed = False
        if model_output > ACTUATOR_MAX or model_output < -ACTUATOR_MAX:
            print(f"Crashed at t={simulation_time}")
            _render_crash(screen, crash_font)
            crashed = True
        _draw_hud(screen)
        _draw_joystick(screen, u)
        _draw_plane(screen, model_output)
        _draw_variables_text(screen, font, simulation_time,
                             model_output, u)
        pygame.display.flip()

        # Stall the rendering for one second so there is time to read
        # the crashed message before the window exits
        if crashed:
            clock.tick(1)
            break

    for _ in pygame.event.get():
        # Empty the event queue to make pygame vanish for good.
        pass
    pygame.quit()
    return np.array(time_tseries), np.array(error_tseries), np.array(control_tseries)


def screen_coordinates_to_pitch(y):
    return -2 * (y - PIXEL_OFFSET_Y_0) / HUD_HEIGHT * ACTUATOR_MAX


def pitch_to_screen_coordinates(p):
    return -p * HUD_HEIGHT / (2 * ACTUATOR_MAX) + PIXEL_OFFSET_Y_0


def _make_pretty_tf(coefficients):
    num_coefs = len(coefficients)
    if num_coefs == 0:
        return "Empty"

    terms = []
    if num_coefs > 1:
        for i in range(0, num_coefs - 1):
            s_idx = num_coefs - 1 - i
            terms.append(f"{coefficients[i]}*s^{s_idx}")
    terms.append(f"{coefficients[-1]}")

    return " + ".join(terms)


def _validate_simulation(plant, controller, disturbance):
    # That plant is of the correct type
    if "TransferFunctionContinuous" not in str(plant):
        print("Error: Plant should be a continuous Transfer Function")
        print(f"But instead it was: {plant}")
        return False

    # Validate the controller will work
    if controller is not None:
        method = getattr(controller, 'update', None)
        if not callable(method):
            print("Error: Controller does not have an 'update' method defined")
            return False
        method = getattr(controller, 'get_control', None)
        if not callable(method):
            print("Error: Controller does not have a 'get_control' method defined")
            return False

    print("Plane transfer function:")
    print(f"num = {_make_pretty_tf(plant.num)}")
    print(f"den = {_make_pretty_tf(plant.den)}")
    if controller is None:
        print(f"Controller type: None")
    else:
        controller_name = str(type(controller)).split("\'")[1].split("\'")[0]
        print(f"Controller type: {controller_name}")

    # --> Also print out transfer function
    # That controller has the right method
    return True


def _draw_hud(surface):
    rect0_l = pygame.Rect(((50, PIXEL_OFFSET_Y_0), (30, 1)))
    rect0_r = pygame.Rect(
        ((SCREEN_WIDTH - 50 - 30, PIXEL_OFFSET_Y_0), (30, 1)))
    pygame.draw.rect(surface, WHITE, rect0_l)
    pygame.draw.rect(surface, WHITE, rect0_r)
    for i in range(10):
        width = 10
        if i == 4:
            width = 20
        if i == 9:
            width = 30
        rect1 = pygame.Rect(
            (50, int(-(i+1) * HUD_HEIGHT / 20) + PIXEL_OFFSET_Y_0), (width, 1))
        rect2 = pygame.Rect(
            (50, int((i+1) * HUD_HEIGHT / 20) + PIXEL_OFFSET_Y_0), (width, 1))
        rect3 = pygame.Rect((SCREEN_WIDTH - 50 - width, int(-(i+1)
                            * HUD_HEIGHT / 20) + PIXEL_OFFSET_Y_0), (width, 1))
        rect4 = pygame.Rect((SCREEN_WIDTH - 50 - width, int((i+1)
                            * HUD_HEIGHT / 20) + PIXEL_OFFSET_Y_0), (width, 1))
        rects = [rect1, rect2, rect3, rect4]
        for rect in rects:
            pygame.draw.rect(surface, GREEN, rect)


def _draw_joystick(surface, pitch):
    y_coord = pitch_to_screen_coordinates(pitch)
    width = 100
    r = pygame.Rect((((SCREEN_WIDTH - width) / 2, y_coord), (width, 1)))
    pygame.draw.rect(surface, CYAN, r)
    pygame.draw.circle(surface, CYAN, (SCREEN_WIDTH / 2, y_coord), 25, 1)


def _draw_plane(surface, pitch):
    y_coord = pitch_to_screen_coordinates(pitch)
    r = pygame.Rect(((100, y_coord), (600, 1)))
    pygame.draw.rect(surface, RED, r)


def _draw_variables_text(surface, font, t, y, u):
    formatted_string = f"t={t:.2f} \t| y(t)={y:.2f} \t| e(t)={-y:.2f} \t| u(t)={u:.2f}"
    text = font.render(formatted_string, True, WHITE)
    surface.blit(text, (5, 0))


def _draw_click_prompt(surface, font, rect):
    text = font.render(
        "Click inside the yellow square to start...", True, WHITE)
    surface.blit(text, (5, 0))
    pygame.draw.rect(surface, YELLOW, rect)


def _render_crash(surface, crash_font):
    text = crash_font.render("CRASHED", True, RED)
    surface.blit(text, (300, PIXEL_OFFSET_Y_0 - 40))


def _handle_event_queue():
    should_exit = False
    for event in pygame.event.get():
        # Todo: handle attempts to close window
        if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
            should_exit = True
    return should_exit


def _wait_for_click(screen, clock, font):
    awaiting_click = True
    rect_width = 50
    rect_height = 50
    click_rectange = pygame.Rect((SCREEN_WIDTH - rect_width) / 2,
                                 PIXEL_OFFSET_Y_0 - rect_height / 2, rect_width, rect_height)
    while awaiting_click:
        user_quit = False
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE or event.type == pygame.QUIT:
                user_quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if click_rectange.collidepoint(mouse_pos):
                    awaiting_click = False

        if user_quit:
            return True
        # Refresh at 60 fps waiting for click
        clock.tick(60)
        screen.fill(BLACK)
        _draw_hud(screen)
        _draw_click_prompt(screen, font, click_rectange)
        pygame.display.flip()
    return False
