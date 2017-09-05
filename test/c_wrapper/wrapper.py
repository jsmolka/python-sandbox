from ctypes import cdll, c_char_p, c_int, POINTER
from random import randint

test_lib = cdll.LoadLibrary("test.so")

# Integer
init = test_lib.init
print("init:", init(randint(0, 100)))

# String
hello = test_lib.hello
hello.restype = c_char_p  # Set expected result type
hello.argtypes = [c_char_p]  # Set expected argument type

s = "Julian"
s = s.encode("utf-8")  # Create bytes
result = hello(s)  # Execute function
result = result.decode("utf-8")  # Convert result back into string
print("hello:", result)

# List / array
ROWS = 10
COLS = 10

array_1d = test_lib.array_1d
array_1d.restype = POINTER(c_int)
array = array_1d(COLS)
l = [array[i] for i in range(0, COLS)]
print("array_1d:", l)

array_2d = test_lib.array_2d
array_2d.restype = POINTER(POINTER(c_int))
array = array_2d(ROWS, COLS)
l = [[array[i][j] for j in range(0, COLS)] for i in range(0, ROWS)]
print("array_2d:")
for row in l:
    print(row)

input()
