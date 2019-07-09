from functools import partial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pycpd import rigid_registration
import numpy as np
import time

def saveNormalizedTxt(Y):

    (rows, columns) = Y.shape
    txt = open("out.txt", "w+")

    for i in range(rows):
        line = ""
        for j in range(columns):
            line += (str(Y[i][j]) + " ")

        txt.write(line + '\n')

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red', label='Target')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue', label='Source')
    ax.text2D(0.87, 0.92, 'Iteration: {:d}\nError: {:06.4f}'.format(iteration, error), horizontalalignment='center',
              verticalalignment='center', transform=ax.transAxes, fontsize='x-large')
    ax.legend(loc='upper left', fontsize='x-large')

    saveNormalizedTxt(Y)
    plt.draw()
    plt.pause(0.001)

def main():
    X = np.loadtxt('groundtruth/Tester_1/Tester_1_pose_0.txt')
    Y = np.loadtxt('data/Tester_1_pose_0_final_frontal.txt') #synthetic data, equaivalent to X + 1

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    callback = partial(visualize, ax=ax)

    reg = rigid_registration(**{ 'X': X, 'Y': Y })
    reg.register(callback)
    plt.show()

if __name__ == '__main__':
    main()
