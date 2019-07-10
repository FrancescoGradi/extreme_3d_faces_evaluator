import Point3D
import matplotlib.pyplot as plt

# data/20140420_011855_News1-Apr-25_final_frontal.txt
# data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt

# Data loading for face 1. The double opening is awful, but python acts kind of dumb here
with open('data/20140420_011855_News1-Apr-25_final_frontal.txt', 'r') as f:
    f1_pts = []
    f1_len = sum(1 for l1 in f)
    f.close()

with open('data/20140420_011855_News1-Apr-25_final_frontal.txt', 'r') as f1:

    for i in range(f1_len):
        line = f1.readline()
        f1_pts.append(Point3D.Point3D(line))

# Data loading for face 2. Same story.
with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f_x:
    f2_pts = []
    f2_len = sum(1 for l2 in f_x)
    f_x.close()

with open('data/03f245cb652c103e1928b1b27028fadd--smith-glasses-too-faced_final_frontal.txt', 'r') as f2:

    for i in range(f2_len):
        line = f2.readline()
        f2_pts.append(Point3D.Point3D(line))

# This computes the minimum distance between each face2_pt and face1_pt. That's the heavy part of the code.
# TODO: look for some optimization
mins = []
for pt2 in f2_pts:
    mins.append(min([pt2.distance(pt1) for pt1 in f1_pts]))

# Splitting a 3D dataset has never been so redundant. I thought that normalized coords would have been better, but
# they don't really change anything.
x_pts = []
y_pts = []
z_pts = []
x_pts2 = []
y_pts2 = []
z_pts2 = []

max_x1 = max([p.x for p in f1_pts])
max_y1 = max([p.y for p in f1_pts])
max_z1 = max([p.z for p in f1_pts])

max_x2 = max([p.x for p in f2_pts])
max_y2 = max([p.y for p in f2_pts])
max_z2 = max([p.z for p in f2_pts])

for pt in f1_pts:
    x_pts.append(pt.x / max_x1)
    y_pts.append(pt.y / max_y1)
    z_pts.append(pt.z / max_z1)

for pt2 in f2_pts:
    x_pts2.append(pt2.x / max_x2)
    y_pts2.append(pt2.y / max_y2)
    z_pts2.append(pt2.z / max_z2)

# Plotting: generating a 3D heatmap of the second face with a point-per-point distance to the first face's points.
# Also, I added a fancy colorbar.
fig = plt.figure()
ax = fig.gca(projection='3d')
AX = ax.scatter(x_pts2, y_pts2, z_pts2, c=mins, cmap='gist_rainbow', lw=0, s=20)
plt.colorbar(AX)
plt.show()