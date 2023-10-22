from scipy.signal import TransferFunction, cont2discrete
import numpy as np


class PlantSimulation:
    def __init__(self, num, den, sample_period, method):
        ss = TransferFunction(num, den).to_ss()
        self.A, self.B, self.C, self.D, _ = cont2discrete(
            (ss.A, ss.B, ss.C, ss.D), sample_period, method=method)
        x_dim = self.A.shape[0]
        self.internal_state = np.zeros(x_dim)
        self.current_output = np.array([0.0])

    def tick(self, plant_input):
        # y[k+1] = Cx[k] + Du[k]
        # x[k+1] = Ax[k] + Bu[k]
        u = np.array([plant_input])
        self.current_output = np.matmul(
            self.C, self.internal_state) + np.matmul(self.D, u)
        self.internal_state = np.matmul(
            self.A, self.internal_state) + np.matmul(self.B, u)

    def get_output(self):
        return self.current_output[0]
