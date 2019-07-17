import h5py
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, isdir, exists
from utils import is_in_range
from utils import uniform_mat_sampling


def matTotxtLandmarks(directory):

    testers = [f for f in listdir(directory) if isdir(join(directory, f))]

    for tester in testers:

        print("Converting file --> " + tester)

        poses = [f for f in listdir(directory + tester + "/cropped_scans/") if
                 isfile(join(directory + tester + "/cropped_scans", f))]

        for pose in poses:
            matlabFiles = {}
            f = h5py.File(directory + tester + "/cropped_scans/" + pose)

            for k, v in f.items():
                matlabFiles[k] = np.array(v)

            if not exists("landmarks/" + tester):
                makedirs("landmarks/" + tester)

            txt = open("landmarks/" + tester + "/" + tester + "_" + pose[:-4] + ".txt", "w+")

            for n in range(len(matlabFiles['lm3d'][0])):
                txt.write(str(- matlabFiles['lm3d'][0][n]) + " " + str(- matlabFiles['lm3d'][1][n]) + " " +
                          str(- matlabFiles['lm3d'][2][n]) + '\n')


def matTotxt(directory, compressionLevel=2, radius=75):

    testers = [f for f in listdir(directory) if isdir(join(directory, f))]

    for tester in testers:

        print("Converting file --> " + tester)

        poses = [f for f in listdir(directory + tester + "/cropped_scans/") if
                 isfile(join(directory + tester + "/cropped_scans", f))]

        for pose in poses:
            print('Converting pose --> ' + pose)
            matlabFiles = {}
            f = h5py.File(directory + tester + "/cropped_scans/" + pose)

            for k, v in f.items():
                matlabFiles[k] = np.array(v)

            if not exists("groundtruth/" + tester):
                makedirs("groundtruth/" + tester)

            txt = open("groundtruth/" + tester + "/" + tester + "_" + pose[:-4] + ".txt", "w+")

            # lm3d sono i landmarks, in particolare il 65-esimo rappresenta la punta del naso.

            x_center = - matlabFiles['lm3d'][0][65]
            y_center = - matlabFiles['lm3d'][1][65]
            z_center = - matlabFiles['lm3d'][2][65]

            pts = []

            for n in range(len(matlabFiles['vertex'][0])):
                if is_in_range(radius, - matlabFiles['vertex'][0][n],
                                       - matlabFiles['vertex'][1][n],
                                       - matlabFiles['vertex'][2][n], x_center, y_center, z_center):
                    pts.append([- matlabFiles['vertex'][0][n],
                               - matlabFiles['vertex'][1][n],
                               - matlabFiles['vertex'][2][n]])

            uniform_mat_sampling(pts, compressionLevel, tester, pose)


compressionLevel = 3
radius = 70

directory = 'faceWarehouse/'
#matTotxt(directory, compressionLevel, radius)
#matTotxtLandmarks(directory)
