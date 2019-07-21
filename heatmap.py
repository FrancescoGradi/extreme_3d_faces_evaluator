import Point3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from alignment_rigid_3D import alignment_rigid
import open3d as o3d
import numpy as np
import copy
from utils import rgb


def generate_heatmap(aligned_cloud_path, gt_path):

    with open(gt_path, 'r') as f:
        f1_pts = []
        f1_len = sum(1 for l1 in f)
        f.close()

    with open(gt_path, 'r') as f1:
        for i in range(f1_len):
            line = f1.readline()
            f1_pts.append(Point3D.Point3D(line))

    with open(aligned_cloud_path, 'r') as f_x:
        f2_pts = []
        f2_len = sum(1 for l2 in f_x)
        f_x.close()

    with open(aligned_cloud_path, 'r') as f2:
        for i in range(f2_len):
            line = f2.readline()
            f2_pts.append(Point3D.Point3D(line))

    mins = []
    for pt2 in f2_pts:
        mins.append(min([pt2.distance(pt1) for pt1 in f1_pts]))

    x1_pts = []
    x2_pts = []
    y1_pts = []
    y2_pts = []
    z1_pts = []
    z2_pts = []

    for pt1 in f1_pts:
        x1_pts.append(pt1.x)
        y1_pts.append(pt1.y)
        z1_pts.append(pt1.z)

    for pt2 in f2_pts:
        x2_pts.append(pt2.x)
        y2_pts.append(pt2.y)
        z2_pts.append(pt2.z)

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 2, 1, projection='3d', title='Logarithmic scale')
    AX = ax.scatter(x2_pts, y2_pts, z2_pts, c=mins, cmap='gist_rainbow',
                    norm=colors.LogNorm(vmin=1, vmax=3), lw=0, s=20)
    plt.colorbar(AX)
    ax = fig.add_subplot(1, 2, 2, projection='3d', title='Linear scale')
    AX = ax.scatter(x2_pts, y2_pts, z2_pts, c=mins, cmap='gist_rainbow', lw=0, s=20)
    plt.colorbar(AX)
    plt.show()


def open3Dheatmap(aligned_cloud_path, gt_path):

    with open(aligned_cloud_path, "r") as ac:
        lines = ac.readlines()

        pointsAC = []
        for line in lines:
            pointsAC.append(Point3D.Point3D(line))

    with open(gt_path, 'r') as gt:
        gt_lines = gt.readlines()
        pointsGT = []
        for gt_line in gt_lines:
            pointsGT.append(Point3D.Point3D(gt_line))

    mins = []
    for pt_ac in pointsAC:
        mins.append(min([pt_ac.distance(pt_gt) for pt_gt in pointsGT]))

    max_mins = max(mins)
    min_mins = min(mins)

    if min_mins > 0.5:
        min_mins = 0

    points = np.zeros((len(lines), 3))
    colours = np.zeros((len(lines), 3))

    i = 0
    for line in lines:
        coords = line.split(sep=" ")

        points[i, 0] = float(coords[0])
        points[i, 1] = float(coords[1])
        points[i, 2] = float(coords[2])

        r, g, b = rgb(val=mins[i], minval=min_mins, maxval=max_mins)

        colours[i, 0] = r / 255
        colours[i, 1] = g / 255
        colours[i, 2] = b / 255

        i += 1

    print("Red --> " + str(min_mins))
    print("Yellow --> " + str((max_mins + min_mins) / 2))
    print("Green --> " + str(max_mins))

    pcd = o3d.geometry.PointCloud()

    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colours)

    o3d.visualization.draw_geometries([pcd])


target = 'groundtruth/Tester_1/Tester_1_pose_1.txt'
source = "data/Tester_1_pose_1_final_frontal.txt"
#alignment_rigid(target, source)

open3Dheatmap("output.txt", target)
