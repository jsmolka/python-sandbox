def defy(*args):
    print(type(args))
    for arg in args:
        print(arg)

defy(1, 2, 3, 4)
