import numpy as np


class ImpulseDisturbance:
    def __init__(self, magnitude):
        self.impulse_magnitude = magnitude
        self.effective_magnitude = None
        self.end_time = None

    def initialise(self, sample_rate_hz, start_time):
        self.effective_magnitude = self.impulse_magnitude * sample_rate_hz
        self.start_time = start_time
        self.end_time = self.start_time + 1 / sample_rate_hz

    def get_disturbance(self, simulation_time):
        assert (self.effective_magnitude != None)
        if simulation_time >= self.start_time and simulation_time < self.end_time:
            return self.effective_magnitude
        else:
            return 0.0


class StepDisturbance:
    def __init__(self, magnitude):
        self.magnitude = magnitude

    def initialise(self, sample_rate_hz, start_time):
        self.start_time = start_time

    def get_disturbance(self, simulation_time):
        if simulation_time >= self.start_time:
            return self.magnitude
        else:
            return 0.0


class SinusoidDisturbance:
    def __init__(self, amplitude, frequency_hz):
        self.amplitude = amplitude
        self.rad_s = frequency_hz * 2 * np.pi

    def initialise(self, sample_rate_hz, start_time):
        self.start_time = start_time

    def get_disturbance(self, simulation_time):
        if simulation_time >= self.start_time:
            t = simulation_time - self.start_time
            return np.sin(t * self.rad_s) * self.amplitude
        else:
            return 0.0


class CompositeDisturbance:
    def __init__(self, disturbances):
        self.disturbances = disturbances

    def initialise(self, sample_rate_hz, start_time):
        for disturbance in self.disturbances:
            disturbance.initialise(sample_rate_hz, start_time)

    def get_disturbance(self, simulation_time):
        total_disturbance = 0.0
        for disturbance in self.disturbances:
            total_disturbance += disturbance.get_disturbance(simulation_time)
        return total_disturbance
