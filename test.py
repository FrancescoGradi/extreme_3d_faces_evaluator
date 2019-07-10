import Point3D
from allignment_rigid_3D import allignment_rigid

# data/20140420_011855_News1-Apr-25_final_frontal.txt
# data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt

# input = "data/Tester_1_pose_0_final_frontal.txt" #distance -> 762.5751153090042
# input = "100Iterations.txt"  #distance -> 8.754972041590518
# input = "150Iterations.txt" #distance -> 8.73787880578837

source = "data/Tester_2_pose_0_final_frontal.txt"

for k in range(1, 21):

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
        mins.append(min(dists))

    print("Distance from tester " + str(k) + " --> " + str(sum(x for x in mins) / len(mins)))
