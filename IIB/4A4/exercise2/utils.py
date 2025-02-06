
import numpy as np
import scipy.signal as cig

import zipfile
import os
import pathlib

working_directory = pathlib.Path(os.path.realpath(__file__)).parent
#cig.find_peaks()

def unzipper(zipf):
    
    with zipfile.ZipFile(zipf, 'r') as zipfopen:
        zipfopen.extractall(working_directory)


unzipper( working_directory / 'data_2024.zip')