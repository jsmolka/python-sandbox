class Parent:
    def __init__(self):
        self.x = "this is x"

    def print_x(self):
        print(self.x)


class ChildA(Parent):
    def __init__(self):
        super(ChildA, self).__init__()
        self.y = "this is y"

    def print_y(self):
        print(self.y)


class ChildB(Parent):
    def __init__(self):
        super(ChildB, self).__init__()
        self.z = "this is z"

    def print_z(self):
        print(self.z)


c_a = ChildA()
c_b = ChildB()

print("ChildA")
try:
    c_a.print_x()
except:
    print("no x function")
try:
    c_a.print_y()
except:
    print("no y function")
try:
    c_a.print_z()
except:
    print("no z function")

print("-------------")

print("ChildB")
try:
    c_b.print_x()
except:
    print("no x function")
try:
    c_b.print_y()
except:
    print("no y function")
try:
    c_b.print_z()
except:
    print("no z function")
	
input()
