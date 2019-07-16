from os import listdir
from os.path import isfile, join
from utils import uniform_sampling

import math


def plyTotxt(directory, compressionLevel=12, radius=25):

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in files:

        print("Processing file --> " + filename)

        uniform_sampling(directory, filename, compressionLevel, radius)


compressionLevel = 16
radius = 70

directory = 'filePlyRete/'
plyTotxt(directory, compressionLevel, radius)

