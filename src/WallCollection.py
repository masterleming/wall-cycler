# WallCollection


class WallCollection:
    def __init__(self, collection=[]):
        self.collection = collection
        self.nextWall = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.collection) == 0:
            raise StopIteration

        index = self.nextWall
        self.nextWall = (self.nextWall + 1) % len(self.collection)
        return self.collection[index]
