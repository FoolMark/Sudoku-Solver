from os import TMP_MAX
from utils import *
from dlx import DLXMap
import numpy as np

def if_valid(i,j,val):
    if ROW[i][val] or COL[j][val] or GRID[rc2g(i,j)][val]:
        return False
    return True

def fit(i,j):
    valid = []
    for v in range(1,10):
        if if_valid(i,j,v) == True:
            valid.append(v)
    return valid
    
def solver_violent(mat,blank,cur):
    if cur == len(blank):
        return mat
    r,c = blank[cur]
    valid = fit(r,c)
    for v in valid:
        ROW[r][v] = COL[c][v] = GRID[rc2g(r,c)][v] = 1
        mat[r][c] = v
        tmp = solver_violent(mat,blank,cur+1)
        if type(tmp) != type(None):
            return tmp  
        ROW[r][v] = COL[c][v] = GRID[rc2g(r,c)][v] = 0
        mat[r][c] = 0
    return None

def solver_DLX(mat):
    Mat = DLXMap(mat)
    Mat.solve()
    return Mat.mat

if __name__ == '__main__':
    origin,blank = getMatrix()
    if checkValid(origin) == False:
        print(f'Invalid matrix... Please check')

    #solution = solver_violent(origin.copy(),blank,0)
    solution = solver_DLX(origin.copy())
    writeMatrix(origin,solution)
    print('Solution Done...')