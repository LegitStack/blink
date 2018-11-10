import inspect

def baz():
    frame_infos = inspect.stack()
    frame = frame_infos[1].frame
    locs = frame.f_locals
    return locs['self']

class Foo():
    def bar(self, func):
        return func()

f1 = Foo()
f2 = f1.bar(baz)
print(f1)
print(f2)
print(f2 is f1)  # True
