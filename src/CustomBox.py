
class CustomBox:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height

    def __str__(self):
        return self.name