from os import listdir
from os.path import isfile, join
from utils import is_in_range
from utils import uniform_sampling


def plyTotxt(directory, compression_level=1):

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in files:

        print("Processing file --> " + filename)

        uniform_sampling(directory, filename, compression_level)

directory = 'filePlyRete/'
plyTotxt(directory, compression_level=20)
