import numpy as np
import math
import time
import re
from sklearn.neighbors import NearestNeighbors


def is_in_range(radius, x, y, z, x_center=-1.8155, y_center=-7.8562, z_center=133.009995):

    if math.sqrt(pow((x - x_center), 2) + pow((y - y_center), 2) + pow((z - z_center), 2)) < radius:
        return True
    else:
        return False


def distances(f_pts, f_len):
    dists = [[] for x in range(f_len)]
    for x in range(f_len):
        for pt2 in f_pts:
            dist = f_pts[x].distance(pt2)
            if dist != 0.0:
                dists[x].append(dist)
    return dists


def uniform_sampling(directory, filename, compression_level=1, radius=25):

    start = time.time()

    f_pts = []

    with open(directory + filename, 'rb') as f:

        lines = f.readlines()
        i = 0

        for line in lines:
            if i < 9:
                i += 1
                continue
            elif line.split()[0] is not b'3':
                text = str(line)
                text = text[2:-3]
                coords = text.split(sep=" ")
                if is_in_range(radius, x=float(coords[0]), y=float(coords[1]), z=float(coords[2])):
                    f_pts.append([float(coords[0]), float(coords[1]), float(coords[2])])

    # This takes care of the '-nan' issue
    if filename == 'Tester_125_pose_0_final_frontal.ply':
        to_pop = []
        for x in range(len(f_pts)):
            if str(f_pts[x][0]) == 'nan':
                to_pop.append(x)
        for x in reversed(to_pop):
            f_pts.pop(x)

    np_f_pts = np.asarray(f_pts, dtype=list)
    print("Length before sampling: " + str(np_f_pts.shape[0]))
    nbrs = NearestNeighbors(n_neighbors=compression_level, algorithm='ball_tree').fit(np_f_pts)
    distances, indices = nbrs.kneighbors(np_f_pts)

    retained_idx = np.ones(np_f_pts.shape[0])
    for i in range(np_f_pts.shape[0]):
        if retained_idx[i] == 1:
            retained_idx[indices[i][2:]] = 0

    decimated_cloud = np_f_pts[retained_idx != 0]

    f_name = re.sub('\.ply$', '', filename)

    with open('data/' + f_name + '.txt', 'w+') as f:
        for el in decimated_cloud:
            if is_in_range(radius, x=float(el[0]), y=float(el[1]), z=float(el[2])):
                f.write(str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + "\n")

    print("Length after sampling: " + str(decimated_cloud.shape[0]))

    print('elapsed time: ' + str(time.time() - start) + ' seconds.')

