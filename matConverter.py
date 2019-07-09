import h5py
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, isdir, exists


def matTotxt(directory):

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

            if not exists("groundtruth/" + tester):
                makedirs("groundtruth/" + tester)

            txt = open("groundtruth/" + tester + "/" + tester + "_" + pose[:-4] + ".txt", "w+")

            for n in range(len(matlabFiles['vertex'][0])):
                txt.write(str(matlabFiles['vertex'][0][n]) + " " +
                          str(matlabFiles['vertex'][1][n]) + " " +
                          str(matlabFiles['vertex'][2][n]) + '\n')


directory = 'faceWarehouse/'
matTotxt(directory)


'''
n = 151
txt = open("faceWarehouseImages.txt", "w+")

for i in range(1, n):
    #for j in range(20):
    txt.write("../faceWarehouse/Tester_" + str(i) + "/TrainingPose/Tester_" + str(i) + "_pose_0" + ".png" + "\n")
    
'''
