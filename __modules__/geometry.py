from panda3d.core import *


def load(form):
    """Defines a cube"""
    forms = ["cube"]

    if form not in forms:
        raise Exception("Wrong form! Available forms: " + str(forms))

    if form == "cube":
        vertex_format = GeomVertexFormat.getV3()
        data = GeomVertexData("vertices", vertex_format, Geom.UHStatic)
        data.setNumRows(8)

        vertex_writer = GeomVertexWriter(data, "vertex")
        # Define cube points / primitives
        vertex_writer.addData3f(0, 0, 0)  # 0
        vertex_writer.addData3f(1, 0, 0)  # 1
        vertex_writer.addData3f(1, 0, 1)  # 2
        vertex_writer.addData3f(0, 0, 1)  # 3

        vertex_writer.addData3f(0, 1, 0)  # 4
        vertex_writer.addData3f(1, 1, 0)  # 5
        vertex_writer.addData3f(1, 1, 1)  # 6
        vertex_writer.addData3f(0, 1, 1)  # 7

        # Connect primitives to triangles
        tri = GeomTriangles(Geom.UHStatic)

        # Front
        tri.addVertex(0)
        tri.addVertex(1)
        tri.addVertex(3)
        tri.closePrimitive()

        tri.addVertex(1)
        tri.addVertex(2)
        tri.addVertex(3)
        tri.closePrimitive()

        # Back
        tri.addVertex(4)
        tri.addVertex(7)
        tri.addVertex(5)
        tri.closePrimitive()

        tri.addVertex(6)
        tri.addVertex(5)
        tri.addVertex(7)
        tri.closePrimitive()

        # Left
        tri.addVertex(0)
        tri.addVertex(3)
        tri.addVertex(4)
        tri.closePrimitive()

        tri.addVertex(7)
        tri.addVertex(4)
        tri.addVertex(3)
        tri.closePrimitive()

        # Right
        tri.addVertex(1)
        tri.addVertex(5)
        tri.addVertex(2)
        tri.closePrimitive()

        tri.addVertex(6)
        tri.addVertex(2)
        tri.addVertex(5)
        tri.closePrimitive()

        # Top
        tri.addVertex(3)
        tri.addVertex(2)
        tri.addVertex(7)
        tri.closePrimitive()

        tri.addVertex(6)
        tri.addVertex(7)
        tri.addVertex(2)
        tri.closePrimitive()

        # Bottom
        tri.addVertex(0)
        tri.addVertex(4)
        tri.addVertex(1)
        tri.closePrimitive()

        tri.addVertex(5)
        tri.addVertex(1)
        tri.addVertex(4)
        tri.closePrimitive()

        # Create cube object
        cube_geometry = Geom(data)
        cube_geometry.addPrimitive(tri)

        # Put cube geometry in Node
        cube = GeomNode(form)
        cube.addGeom(cube_geometry)
        return cube

# Use geometry
# object = self.render.attachNewNode(geometry.load(form))
# object.setScale(size, size, size)
# object.setPos(x, y, z)
# object.setColor(r, g, b)
