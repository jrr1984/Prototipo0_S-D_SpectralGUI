def hola():
    for i in range(3):
        print(i)
        yield i*i

hola()
