import numpy as np
import os
from utils import *
if __name__ == '__main__':
    os.system('python cv_solution/gridSplit.py')
    labels = np.load('input_label.npy').reshape(9,9)
    writeMatrixFromImage(labels)
    os.system('python solve.py')