from os import listdir, remove
from os.path import isfile, join
from utils import uniform_sampling

import math


def plyTotxt(directory, compressionLevel=72, radius=70):

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in files:

        print("Processing file --> " + filename)

        uniform_sampling(directory, filename, compressionLevel, radius)


directory = 'filePlyRete/'
plyTotxt(directory)
