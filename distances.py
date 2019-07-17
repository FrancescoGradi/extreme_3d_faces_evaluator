import Point3D
import numpy as np
from scipy.spatial.distance import directed_hausdorff


def averageDistance(target, source):

    with open(source, 'r') as f:
        f1_pts = []
        f1_len = sum(1 for l1 in f)
        f.close()

    with open(source, 'r') as f1:

        for i in range(f1_len):
            line = f1.readline()
            f1_pts.append(Point3D.Point3D(line))

    with open(target, 'r') as f_x:
        f2_pts = []
        f2_len = sum(1 for l2 in f_x)
        f_x.close()

    with open(target, 'r') as f2:

        for i in range(f2_len):
            line = f2.readline()
            f2_pts.append(Point3D.Point3D(line))

    mins = []
    for pt in f1_pts:
        dists = []
        for pt2 in f2_pts:
            dists.append(pt.distance(pt2))
        mins.append(min(dists))

    # return min, average, max, median

    return min(mins), sum(x for x in mins) / len(mins), max(mins), np.median(mins)


def hausdorffDistance(target, source):

    gt = np.array([[0, 0, 0]])

    with open(target, "r") as g1:
        for line in g1:
            line = line.split(sep=" ")
            row = np.array([float(line[0]), float(line[1]), float(line[2][:-2])])
            gt = np.append(gt, [row], axis=0)

    gt = np.delete(gt, 0, 0)

    data = np.array([[0, 0, 0]])

    with open(source, "r") as d1:
        for line in d1:
            line = line.split(sep=" ")
            row = np.array([float(line[0]), float(line[1]), float(line[2][:-2])])
            data = np.append(data, [row], axis=0)

    data = np.delete(gt, 0, 0)

    return directed_hausdorff(gt, data)[0]
