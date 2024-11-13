class DrawLabelsData:
    def __init__(self, image, labels):
        self.image = image
        self.labels = labels

class ImageDrawed:
    def __init__(self, image, free_spaces, occupied_spaces):
        self.image = image
        self.free_spaces = free_spaces
        self.occupied_spaces = occupied_spaces

