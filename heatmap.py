import Point3D
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from alignment_rigid_3D import alignment_rigid
import open3d as o3d


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

        print(mins)

        with open("heatmap.pcd", "w+") as hm:
            hm.write("VERSION .7" + "\n")
            hm.write("FIELDS x y z rgb" + "\n")
            hm.write("POINTS " + str(len(lines)) + "\n")
            hm.write("DATA ascii" + "\n")

            i = 0
            for line in lines:
                coords = line.split(sep=" ")
                hm.write(coords[0] + " " + coords[1] + " " + coords[2] + " " + str(mins[i]) + "\n")
                i += 1

        pcd = o3d.io.read_point_cloud("heatmap.pcd")
        o3d.visualization.draw_geometries([pcd])


target = 'groundtruth/Tester_1/Tester_1_pose_0.txt'
source = "data/Tester_1_pose_0_final_frontal.txt"
#alignment_rigid(target, source)
#generate_heatmap('output.txt', target)

#pcd = o3d.io.read_point_cloud("data/Tester_1_pose_0_final_frontal.pcd")
#o3d.visualization.draw_geometries([pcd])

open3Dheatmap("output.txt", target)