import time

import numpy as np

import matConverter
import plyConverter
from distances import averageDistance, hausdorffDistance
from alignment_rigid_3D import alignment_rigid, max_iterations


def classification_test(testers, distance=None):

    start = time.time()

    with open("classificationTestResults.txt", "w+") as tr:

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

                print("Alignment with " + str(k))

                groundtruth = "groundtruth/Tester_" + str(k) + "/Tester_" + str(k) + "_pose_0.txt"

                alignment_rigid(target=groundtruth, source=source)

                print("Calculating distance")

                if distance == "hausdorff":
                    distTot = hausdorffDistance(target=groundtruth, source="output.txt")
                else:
                    distTot = averageDistance(target=groundtruth, source="output.txt")[1]

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
        tr.write("Elapsed time: " + str(end - start))


def distancesTest(testers, poses):

    start = time.time()

    with open("distancesTestResult.txt", "w+") as tr:

        tr.write("Parameters: " + "\n")
        tr.write("-max_iterations = " + str(max_iterations) + "\n")
        tr.write("-compressionLevel = " + str(plyConverter.compressionLevel) + ", " + str(matConverter.compressionLevel)
                 + "\n")
        tr.write("-radius from nose = " + str(plyConverter.radius) + "\n")

        for tester in testers:
            for pose in poses:

                source = "data/Tester_" + str(tester) + "_pose_" + str(pose) + "_final_frontal.txt"
                target = "groundtruth/Tester_" + str(tester) + "/Tester_" + str(tester) + "_pose_" + str(pose) + ".txt"

                tr.write("\n")
                tr.write("\n")
                tr.write("Tester " + str(tester) + " with pose " + str(pose) + "\n")

                tr.write("\n")
                tr.write("Distances from groundtruth to source:" + "\n")

                print("Alignment " + str(tester) + " with pose " + str(pose))

                alignment_rigid(target, source)

                print("Distance calculation of " + str(tester) + " with pose " + str(pose)
                      + " from groundtruth to source")

                mn, avg, mx, median = averageDistance(target, "output.txt")

                tr.write("Min --> " + str(mn) + "\n")
                tr.write("Average --> " + str(avg) + "\n")
                tr.write("Max --> " + str(mx) + "\n")
                tr.write("Median --> " + str(median) + "\n")

                tr.write("\n")
                tr.write("Distances from source to groundtruth:" + "\n")

                print("Distance calculation of " + str(tester) + " with pose " + str(pose)
                      + " from source to groundtruth")

                mn, avg, mx, median = averageDistance("output.txt", target)

                tr.write("Min --> " + str(mn) + "\n")
                tr.write("Average --> " + str(avg) + "\n")
                tr.write("Max --> " + str(mx) + "\n")
                tr.write("Median --> " + str(median) + "\n")

        end = time.time()
        print(str(end - start))
        tr.write("\n")
        tr.write("\n")
        tr.write("Time elapsed: " + str(end - start))


caucasians = range(101, 111)
#caucasians = range(1, 2)
poses = [0]

#classification_test(caucasians)

distancesTest(caucasians, poses)
