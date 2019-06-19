
class MissingCifData():
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value
