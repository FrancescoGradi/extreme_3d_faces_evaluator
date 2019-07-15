import time

import numpy as np

import matConverter
import plyConverter
from distances import averageDistance, hausdorffDistance
from alignment_rigid_3D import alignment_rigid, max_iterations


def classification_test(testers, distance=None):

    start = time.time()

    with open("testResults.txt", "w+") as tr:

        tr.write("Parameters: " + "\n")
        tr.write("-max_iterations = " + str(max_iterations) + "\n")
        tr.write("-compressionLevel = " + str(plyConverter.compressionLevel) + ", " + str(matConverter.compressionLevel)
                 + "\n")
        tr.write("-radius from nose = " + str(plyConverter.radius) + "\n")

        if distance == "hausdorff":
            tr.write("-hausdorff" + "\n")

        truePositives = []

        for tester in testers:

            source = "data/Tester_" + str(tester) + "_pose_0_final_frontal.txt"
            results = dict()

            tr.write('\n')
            tr.write("Reference:    " + source[5:15] + '\n')

            for k in testers:

                print("Ground truth image " + str(k))

                groundtruth = "groundtruth/Tester_" + str(k) + "/Tester_" + str(k) + "_pose_0.txt"

                alignment_rigid(target=groundtruth, source=source)

                print("Calculating distance")

                if distance == "hausdorff":
                    distTot = hausdorffDistance(target=groundtruth, source="output.txt")
                else:
                    distTot = averageDistance(target=groundtruth, source="output.txt")

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
        tr.write("Success rate --> " + str((len(truePositives) / len(testers)) * 100) + "\n")

        end = time.time()
        print(str(end - start))
        tr.write("Time elapsed: " + str(end - start))


#caucasians = range(101, 142)
caucasians = range(101, 103)

classification_test(caucasians)