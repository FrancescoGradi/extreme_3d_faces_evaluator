import time

import numpy as np

import Point3D
import matConverter
import plyConverter
from allignment_rigid_3D import allignment_rigid, max_iterations

# data/20140420_011855_News1-Apr-25_final_frontal.txt
# data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt

# input = "data/Tester_1_pose_0_final_frontal.txt" #distance -> 762.5751153090042
# input = "100Iterations.txt"  #distance -> 8.754972041590518
# input = "150Iterations.txt" #distance -> 8.73787880578837

threshold = 4

#caucasians = range(101, 142)
caucasians = range(101, 104)

start = time.time()

with open("testResults.txt", "w+") as tr:

    tr.write("Parameters: " + "\n")
    tr.write("-threshold = " + str(threshold) + "\n")
    tr.write("-max_iterations = " + str(max_iterations) + "\n")
    tr.write("-compressionLevel = " + str(plyConverter.compressionLevel) + ", " + str(matConverter.compressionLevel)
             + "\n")

    truePositives = []

    for tester in caucasians:

        source = "data/Tester_" + str(tester) + "_pose_0_final_frontal.txt"
        results = dict()

        tr.write('\n')
        tr.write("Reference:    " + source[5:15] + '\n')

        for k in caucasians:

            print("Ground truth image " + str(k))

            groundtruth = "groundtruth/Tester_" + str(k) + "/Tester_" + str(k) + "_pose_0.txt"

            allignment_rigid(target=groundtruth, source=source)

            with open("output.txt", 'r') as f:
                f1_pts = []
                f1_len = sum(1 for l1 in f)
                f.close()

            with open("output.txt", 'r') as f1:

                for i in range(f1_len):
                    line = f1.readline()
                    f1_pts.append(Point3D.Point3D(line))

            with open(groundtruth, 'r') as f_x:
                f2_pts = []
                f2_len = sum(1 for l2 in f_x)
                f_x.close()

            with open(groundtruth, 'r') as f2:

                for i in range(f2_len):
                    line = f2.readline()
                    f2_pts.append(Point3D.Point3D(line))

            print("Distance calculating")

            mins = []
            for pt in f1_pts:
                dists = []
                for pt2 in f2_pts:
                    dists.append(pt.distance(pt2))
                if min(dists) < threshold:
                    mins.append(min(dists))

            distTot = sum(x for x in mins) / len(mins)
            results[k] = distTot

            line = "Distance from tester " + str(k) + " --> " + str(distTot)

            print(line)
            tr.write(line + '\n')

        argMin = np.infty
        minDist = np.infty
        for key in results.keys():
            if results[key] < minDist:
                minDist = results[key]
                argMin = key

        if argMin == tester:
            tr.write("Corrected classification of tester " + str(tester) + "\n")
            truePositives.append(argMin)
        else:
            tr.write("Wrong classification of tester " + str(tester) + " with tester " + str(argMin) + "\n")

    tr.write("\n")
    tr.write("Success rate --> " + str((len(truePositives) / len(caucasians)) * 100) + "\n")

    end = time.time()
    print(str(end - start))
    tr.write("Time elapsed: " + str(end - start))
