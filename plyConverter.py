from os import listdir, remove
from os.path import isfile, join
from utils import uniform_sampling

import math


def plyTotxt(directory, compressionLevel=12, radius=25):

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in files:

        print("Processing file --> " + filename)

        uniform_sampling(directory, filename, compressionLevel, radius)


compressionLevel = 72
radius = 70

directory = 'filePlyRete/'
#plyTotxt(directory, compressionLevel, radius)

"""
n = 151
txt = open("faceWarehouseImages.txt", "w+")
for i in range(138, n):
    for j in range(20):
        txt.write("../faceWarehouse/Tester_" + str(i) + "/TrainingPose/Tester_" + str(i) + "_pose_" + str(j) + ".png" + "\n")


files = [f for f in listdir(directory) if isfile(join(directory, f))]

for file in files:
    if (file[-17:] == "final_frontal.ply"):
        continue
    else:
        remove(directory + file)
        
"""