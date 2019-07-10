from os import listdir
from os.path import isfile, join


def plyTotxt(directory, compressionLevel=12):

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    for filename in files:

        print("Processing file --> " + filename)

        with open(directory + filename, 'rb') as ply:

            txt = open("data/" + filename[:-4] + ".txt", "w+")

            if b'ply' not in ply.readline():
                raise ValueError('The file does not start whith the word ply')

            lines = ply.readlines()

            i = 0
            j = 0

            for line in lines:
                if i < 9:
                    i += 1
                    continue

                elif line.split()[0] is not b'3' and (j % compressionLevel) == 0:
                    text = str(line)
                    txt.write(text[2:-3] + '\n')

                j += 1


directory = 'filePlyRete/'
plyTotxt(directory, 24)