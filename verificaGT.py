
directory = "filePlyRete/"

testers = range(76, 151)
poses = range(20)

for tester in testers:
    for pose in poses:
        try:
            with open(directory + "Tester_" + str(tester) + "_pose_" + str(pose) + "_final_frontal.ply", "r") as fl:
                continue
        except:
            print("Manca il file: " + str(tester) + " " + str(pose))

"""

from os import listdir, makedirs
from os.path import isfile, join, isdir, exists

directory = "groundtruth/"

testers = range(1, 151)
poses = range(20)

for tester in testers:
    for pose in poses:

        try:
            with open(directory + "Tester_" + str(tester) + "/" + "Tester_" + str(tester) + "_pose_" + str(pose) +
                      ".txt", "r") as fl:
                continue
        except:
            print("Manca il file: " + str(tester) + " " + str(pose))
            
"""