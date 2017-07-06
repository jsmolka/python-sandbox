import geometry

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

# Configuration
size = 5


class MyApp(ShowBase):
    def __init__(self):
        global size
        ShowBase.__init__(self)

        cube = self.render.attachNewNode(geometry.load("cube"))
        cube.setScale(size, size, size)
        cube.setPos(0, 0, 0)
        cube.setColor(255, 255, 255)
        cube.reparentTo(self.render)

        # Task
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        global size
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians) + size / 2, -20.0 * cos(angleRadians) + size / 2, 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
