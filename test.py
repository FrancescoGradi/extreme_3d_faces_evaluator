import Point3D


# data/20140420_011855_News1-Apr-25_final_frontal.txt
# data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt

with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f:
    f1_pts = []
    f1_len = sum(1 for l1 in f)
    f.close()

with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f1:

    for i in range(f1_len):
        line = f1.readline()
        f1_pts.append(Point3D.Point3D(line))


with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f_x:
    f2_pts = []
    f2_len = sum(1 for l2 in f_x)
    f_x.close()

with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f2:

    for i in range(f2_len):
        line = f2.readline()
        f2_pts.append(Point3D.Point3D(line))

mins = []
for pt in f1_pts:
    dists = []
    for pt2 in f2_pts:
        dists.append(pt.distance(pt2))
    mins.append(min(dists))

print((sum(x for x in mins) / len(mins)))