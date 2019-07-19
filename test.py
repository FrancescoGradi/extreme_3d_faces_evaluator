import time
import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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

        analytics = {}

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

                distancesDict = {}

                print("Distance calculation of Tester " + str(tester) + " with pose " + str(pose)
                      + " from groundtruth to source")

                mn, avg, mx, median = averageDistance(target, "output.txt")
                hausdorff = hausdorffDistance(target, "output.txt")

                tr.write("Min --> " + str(mn) + "\n")
                tr.write("Average --> " + str(avg) + "\n")
                tr.write("Max --> " + str(mx) + "\n")
                tr.write("Median --> " + str(median) + "\n")
                tr.write("Hausdorff distance --> " + str(hausdorff) + "\n")

                distancesDict["min_sg"] = mn
                distancesDict["avg_sg"] = avg
                distancesDict["max_sg"] = mx
                distancesDict["median_sg"] = median
                distancesDict["hausdorff_sg"] = hausdorff

                tr.write("\n")
                tr.write("Distances from source to groundtruth:" + "\n")

                print("Distance calculation of Tester " + str(tester) + " with pose " + str(pose)
                      + " from source to groundtruth")

                mn, avg, mx, median = averageDistance("output.txt", target)
                hausdorff = hausdorffDistance("output.txt", target)

                tr.write("Min --> " + str(mn) + "\n")
                tr.write("Average --> " + str(avg) + "\n")
                tr.write("Max --> " + str(mx) + "\n")
                tr.write("Median --> " + str(median) + "\n")
                tr.write("Hausdorff distance --> " + str(hausdorff) + "\n")

                distancesDict["min_gs"] = mn
                distancesDict["avg_gs"] = avg
                distancesDict["max_gs"] = mx
                distancesDict["median_gs"] = median
                distancesDict["hausdorff_gs"] = hausdorff

                analytics["Tester_" + str(tester) + "_pose_" + str(pose)] = distancesDict

        end = time.time()
        print(str(end - start))
        tr.write("\n")
        tr.write("\n")
        tr.write("Time elapsed: " + str(end - start))

        with open("analytics.json", "w+") as aj:
            json.dump(analytics, aj, indent=4)


def posesPrecision(testers, poses):

    with open("analytics.json", "r") as an:
        analytics = json.load(an)

        # Dizionario che contiene tutti i valori di riferimento della media delle distanze, in particolare viene preso
        # come refernce la pose 0 (espressione neutra)

        references = {}
        for tester in testers:
            avg_gs = analytics["Tester_" + str(tester) + "_pose_0"]["avg_gs"]
            avg_sg = analytics["Tester_" + str(tester) + "_pose_0"]["avg_sg"]

            references[tester] = (avg_gs + avg_sg)/2

        sum = 0
        for key in references.keys():
            sum += references[key]

        print(sum/(len(references.keys())))

        # Per ogni posa calcola il rapporto con la media delle distanze medie di ciascun tester e rende una percentuale
        # la quale rappresenta quanto rappresenta bene la posa rispetto al valore di riferimento (espressione neutra)

        posesPercentage = []
        for pose in poses[1:]:
            poseAverage = 0
            for tester in testers:
                avg_gs = analytics["Tester_" + str(tester) + "_pose_" + str(pose)]["avg_gs"]
                avg_sg = analytics["Tester_" + str(tester) + "_pose_" + str(pose)]["avg_sg"]

                poseAverage += (((avg_gs + avg_sg)/2)/references[tester]) - 1
            posesPercentage.append((poseAverage/len(testers)) * 100)

        colors = []
        for pose in posesPercentage:
            if pose <= 5:
                colors.append("green")
            elif 5 < pose < 10:
                colors.append("limegreen")
            elif 10 < pose < 20:
                colors.append("yellow")
            elif 20 <= pose < 30:
                colors.append("orange")
            elif pose >= 30:
                colors.append("red")

        fig, ax = plt.subplots()

        bars = plt.bar(x=np.asarray(poses[1:]), height=np.asarray(posesPercentage))
        plt.xticks(np.asarray(poses[1:]))
        plt.ylabel("Deviation from reference")
        plt.xlabel("Poses")

        for i in range(len(colors)):
            bars[i].set_color(colors[i])

        formatter = FuncFormatter(lambda y, pos: "%d%%" % (y))
        ax.yaxis.set_major_formatter(formatter)

        plt.title("Poses percentage precision")
        plt.show()


#caucasians = range(101, 111)
#caucasians = range(76, 151)
poses = range(20)

testers = []
for i in range(101, 142):
    if i is not 89:
        testers.append(i)

posesPrecision(testers, poses)

#classification_test(caucasians)

#distancesTest(caucasians, poses)
