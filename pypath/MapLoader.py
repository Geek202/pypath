# import PIL.Image

class MapLoaderCSV:
    def __init__(self, mapfile):
        self.mapfile = mapfile
        self.map = []

    def load(self):
        with open(self.mapfile) as f:
            data = f.readlines()
        for ln in data:
            line = ln.strip()
            self.map.append(line.split(","))

        tmp = self.map.copy()
        for x in range(len(tmp)):
            for y in range(len(tmp[0])):
                if type(self.map[x][y]) is not int:
                    print("NOT INT!")
                    tmp[x][y] = int(self.map[x][y])

        self.map = tmp.copy()

        print(self.map)

    def getMap(self):
        if len(self.map) != 0:
            return self.map.copy()
        else:
            self.load()
            return self.map.copy()

'''
class MapLoaderImage:
    def __init__(self, mapimg):
        self.mapimg = mapimg
        self.map = []

    def load(self):
        self.img = PIL.Image.open(self.mapimg)
        pix = self.img.load()
        self.map = [[0] * self.img.width] * self.img.height
        for y in range(self.img.height):
            for x in range(self.img.width):
                print(pix[x, y])
                if pix[x, y][3] == 255:
                    print("{0} is solid".format((x, y)))
                    self.map[x][y] = 1
                else:
                    print("{0} is empty".format((x, y)))
                    self.map[x][y] = 0
        self.img.close()
    def getMap(self):
        if len(self.map) != 0:
            return self.map.copy()
        else:
            self.load()
            return self.map
'''
