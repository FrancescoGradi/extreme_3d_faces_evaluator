import Point3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D


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

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    AX = ax.scatter(x2_pts, y2_pts, z2_pts, c=mins, cmap='gist_rainbow',
                    norm=colors.LogNorm(vmin=min(mins), vmax=max(mins)), lw=0, s=20)
    plt.colorbar(AX)
    plt.show()


generate_heatmap("output.txt", "groundtruth/Tester_1/Tester_1_pose_0.txt")
