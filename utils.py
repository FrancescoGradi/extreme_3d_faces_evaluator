import Point3D
import numpy as np

def uniform_sampling(file_path):

    f_pts = []

    with open(file_path, 'r') as f:
        f_len = sum(1 for l in f)
        f.close()

    with open(file_path, 'r') as f:
        for x in range(f_len):
            line = f.readline()
            f_pts.append(Point3D.Point3D(line))

    dists = [[] for x in range(f_len)]
    for x in range(f_len):
        for pt2 in f_pts:
            dist = f_pts[x].distance(pt2)
            if dist != 0.0:
                dists[x].append(dist)

    print("Length before sampling: " + str(len(dists)))
    for dist_array in dists:
        np_dist = np.array(dist_array)
        indices = np.argsort(np_dist)[:12]
        for x in indices:
            if x < len(dists):
                dists.pop(x)

    print("Length after sampling: " + str(len(dists)))

uniform_sampling('output.txt')