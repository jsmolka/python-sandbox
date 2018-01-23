import capi
import random

pth = capi.pydir("argtypes.dll")


@capi.cfunc
def arg_int(i, dll=pth): 
    pass
    
    
@capi.cfunc
def arg_double(d, dll=pth): 
    pass


@capi.cfunc
def arg_string(s, dll=pth): 
    pass
    
    
@capi.cfunc
def arg_list_int(l, i, dll=pth):
    pass
    
    
@capi.cfunc
def arg_list_double(l, i, dll=pth):
    pass
    
    
@capi.cfunc
def arg_list_2d(l, r, c, dll=pth):
    pass


arg_int(50)
arg_double(100.5)
arg_string("Test")
arg_list_int([1, 2, 3], 3)
arg_list_double([1.2, 3.4, 5.6, 7.8], 4)

n = 10
l = [[random.randint(100, 999) for i in range(n)] for j in range(n)]        
arg_list_2d(l, n, n)
