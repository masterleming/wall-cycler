# WallCollection

class WallCollection:
    def __init__(self):
        self.collection = []
        self.nextWall = 0

    def next(self):
        if len(self.collection) == 0:
            raise Exception(
                'Cannot get next wallpaper! The collection is empty')

        index = self.nextWall
        self.nextWall = (self.nextWall + 1) % len(self.collection)
        return self.collection[index]

    def update(self, files=[]):
        tmpCollection = set(self.collection)
        newFiles = [f for f in files if f not in tmpCollection]
        self.collection[self.nextWall:self.nextWall] = newFiles
