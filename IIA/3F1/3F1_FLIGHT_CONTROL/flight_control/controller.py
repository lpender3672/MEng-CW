import os
# Stop pygame spamming the console when imported
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np
from flight_control.simulation import screen_coordinates_to_pitch, ACTUATOR_MAX

DEADZONE_SIZE = 0.05

class ManualControl():
    def __init__(self):
        self.current_control = 0.0

    def update(self, error_signal, delta_t):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.current_control = screen_coordinates_to_pitch(mouse_y)
        self.current_control = np.clip(self.current_control, -ACTUATOR_MAX, ACTUATOR_MAX)

        # Add a deadzone near 0.0 so that a slightly off-centre mouse position
        # does not induce a slow drift
        if np.abs(self.current_control) < DEADZONE_SIZE:
            self.current_control = 0.0

    def get_control(self):
        return self.current_control
