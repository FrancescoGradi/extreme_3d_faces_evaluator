from os import listdir, rename
from os.path import isfile, join, isdir

directory = "faceWarehouse/"
testers = [f for f in listdir(directory) if isdir(join(directory, f))]

for tester in testers:
    poses = [f for f in listdir(directory + tester + "/TrainingPose/") if
                    isfile(join(directory + tester + "/TrainingPose", f))]

    for pose in poses:
        if pose[-4:] == ".png":
            old = join(directory + tester + "/TrainingPose/", pose)
            new = join(directory + tester + "/TrainingPose/", tester + "_" + pose)
            rename(old, new)
