import os
import numpy as np
from matplotlib import pyplot as plt


def main():

    m1 = 2.55 
    k1 = 1458.7  # strucutre stiffness
    l1 = 1.98  # structure damping

    m2 = 0.05  # tuned mass damper mass
    k2 = 28.6  # tuned mass damper stiffness to match structure
    l2 = 0.1 # tuned mass damper damping

    print(np.sqrt(k1/m1))

    os.system(f'py IB/Extended_Coursework/a1.py --m1 {m1} --k1 {k1} --l1 {l1} --m2 {m2} --k2 {k2} --l2 {l2}')



if __name__ == '__main__':
    main()