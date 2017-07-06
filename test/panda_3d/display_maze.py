import geometry
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from maze import *

pos = 0
iteration = 1
m = Maze()
m.create(20, 20, Algorithm.Create.BACKTRACKING)
size = 5
x = z = int((len(m.maze) * size) / 2)


class MyApp(ShowBase):
    def __init__(self):
        global m, size
        ShowBase.__init__(self)

        # Load the box model
        for i in range(0, len(m.maze)):
            for j in range(0, len(m.maze[0])):
                if m.maze[i, j, 0] == 0:
                    cube = self.render.attachNewNode(geometry.load("cube"))
                    cube.setPos(i * size, 0, j * size)
                    cube.setScale(size, size, size)
                    cube.setColor(255, 255, 255)
                    cube.reparentTo(self.render)

        # Set camera position
        self.disable_mouse()  # Only way to set the camera position
        # Set task to print camera position
        self.taskMgr.add(self.camera_position, "camera_position")

    def camera_position(self, task):
        global iteration, pos, x, z
        pos -= iteration
        self.camera.setPos(x, pos, z)
        print(self.camera.getPos())
        return Task.cont


app = MyApp()
app.run()
