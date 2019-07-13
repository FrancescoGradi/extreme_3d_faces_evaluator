import math

class Point3D:

    def __init__(self, coords_str):

        coords = coords_str.split(sep=" ")
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.z = float(coords[2])

    def isEqual(self, point):

        if self.x == point.x and self.y == point.y and self.z == point.z:
            return True
        else:
            return False

    def distance(self, point):

        return math.sqrt(pow((self.x - point.x), 2) + pow((self.y - point.y), 2) + pow((self.z - point.z), 2))