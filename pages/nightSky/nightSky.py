# Port to pyscript/p5js by Ben Alkov, 2022-07-05
# Port to Processing.py by Ben Alkov, 2014-07-10 - 2014-10-17:
# https://github.com/tildebyte/processing.py-demos/blob/7fd0c8900c175ea1fe2089eaf5c61ffed5922999/nightSky/nightSky.pyde
# From patakk's nightSky, 15 February, 2014
# https://patakk.tumblr.com/nightSky

class Point(object):
    HalfWidth = 0
    HalfHeight = 0
    HalfDist = 0
    Limit = 0

    def __init__(self, index):
        self.index = index
        self.startX = 0
        self.startY = 0
        self.rnd = random(5, 30)
        self.diameter = map(self.rnd, 5, 30, 0.5, 2)
        if random(1) > 0.5:
            self.rt = True
        else:
            self.rt = False
        self.phi = random(360)
        self.x = 0
        self.y = 0
        self.lines = []
        self.makePoint()

    def makePoint(self):
        while True:
            randX = random(Point.HalfWidth * 0.74) + random(40)
            randY = random(Point.HalfHeight * 0.84) + random(40)
            angle = random(2 * PI)
            initX = randX * cos(angle)
            initY = randY * sin(angle)
            dx = map(initX,
                     0, Point.HalfWidth, 0, 1.15)
            dy = map(initY,
                     0, Point.HalfHeight, 0, 1.35)
            prob = pow(2.72, -(dx**2 * 2 + dy**2 * 2))
            if random(1) < prob:
                self.startX = initX
                self.startY = initY
                return

    def setLines(self, others):
        # for other in others:
        #     if (self is not other
        #             and dist(self.x, self.y, other.x, other.y) < Limit / 3):
        #         lines.append(PVector(self.index,
        #                              other.index))
        thirdLimit = Point.Limit / 3
        self.lines = [other.index
                      for other in others
                      if (self is not other
                          and dist(self.x, self.y, other.x, other.y) < thirdLimit)]

    def update(self, time, others):
        if self.rt:
            self.x = self._calc(self.startX, cos, time)
            self.y = self._calc(self.startY, sin, time)
        else:
            self.x = self._calc(self.startX, cos, -time)
            self.y = self._calc(self.startY, sin, -time)
        noStroke()
        fill(255)
        ellipse(self.x, self.y, self.diameter, self.diameter)
        self.drawLines(others)

    def drawLines(self, others):
        halfLimit = Point.Limit / 2
        for other in others:
            if (self is not other
                    and other.index in self.lines):
                plusX = self.x + other.x * 0.5
                plusY = self.y + other.y * 0.5
                mouseWrapX = mouseX - Point.HalfWidth
                mouseWrapY = mouseY - Point.HalfHeight
                amp = (map(dist(plusX, plusY, 0, 0),
                           0, Point.HalfDist, 2, 8))
                distance = (map(noise(plusX * 0.03, plusY * 0.03),
                                0, 1, 5, halfLimit))
                if dist(plusX, plusY, mouseWrapX, mouseWrapY) < Point.Limit:
                    distance = (distance * map(dist(plusX, plusY, mouseWrapX, mouseWrapY),
                                               0, Point.Limit, amp, 1))
                if dist(self.x, self.y, other.x, other.y) < distance:
                    opacity = map(dist(self.x, self.y, other.x, other.y),
                                  0, distance, 85, 0)
                    stroke(255, opacity)
                    line(self.x, self.y, other.x, other.y)

    def _calc(self, coord, func, time):
        return coord + self.rnd * func(radians(time * self.diameter + self.phi))



SketchWidth = 700
SketchHeight = 300
Point.HalfWidth = SketchWidth / 2
Point.HalfHeight = SketchHeight / 2
Point.HalfDist = dist(0, 0, Point.HalfWidth, Point.HalfHeight)
MagicNumber = dist(0, 0, 960, 540)
NumPoints = (500.0 * Point.HalfDist / MagicNumber)
Point.Limit = (160.0 * Point.HalfDist / MagicNumber)
points = []


def setup():
    global points
    size(SketchWidth, SketchHeight)
    background(0)
    smooth()
    strokeWeight(0.8)
    points = [Point(index) for index in range(NumPoints)]
    for _point in points:
        _point.setLines(points)


def draw():
    background(0)
    translate(Point.HalfWidth, Point.HalfHeight)
    for _point in points:
        _point.update(frameCount, points)