class BoundingBox:

    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Page:
    """A page!"""

    def __init__(self, element):
        self.index = 0
        self.bbox = BoundingBox()
