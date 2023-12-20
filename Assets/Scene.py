from Assets.shapesCollections import PointsCollection, LinesCollection, RectsCollection


class Scene:
    def __init__(self, points: PointsCollection | None = None, lines: LinesCollection | None = None,
                 rects: RectsCollection | None = None):
        self.__points = points if points is not None else PointsCollection([])
        self.__lines = lines if lines is not None else LinesCollection([])
        self.__rects = rects if rects is not None else RectsCollection([])

    @property
    def points(self):
        return self.__points

    @property
    def lines(self):
        return self.__lines

    @property
    def rects(self):
        return self.__rects
