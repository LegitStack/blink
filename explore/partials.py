from functools import partial

def function_a():
    return 10

def function_b(fa):
    return fa * 3

def function_c(fa, fb):
    return fa + fb

abc = partial(function_a)
print(abc)
print(abc())
print(dir(abc))

abc = partial(function_c, function_a())

print('\n', 'args', abc.args)  # existing args
#print('\n', 'func', abc.func())
print('\n', 'keywords', abc.keywords)
#print('\n', '__call__', abc.__call__())
#print('\n', '__class__', abc.__class__())
#print('\n', '__delattr__', abc.__delattr__())
print('\n', '__dict__', abc.__dict__)
print('\n', '__dir__', abc.__dir__())
print('\n', '__doc__', abc.__doc__)
#print('\n', '__eq__', abc.__eq__())
print('\n', '__format__', abc.__format__())
print('\n', '__ge__', abc.__ge__())
print('\n', '__getattribute__', abc.__getattribute__())
print('\n', '__gt__', abc.__gt__())
print('\n', '__hash__', abc.__hash__())
print('\n', '__init__', abc.__init__())
print('\n', '__init_subclass__', abc.__init_subclass__())
print('\n', '__le__', abc.__le__())
print('\n', '__lt__', abc.__lt__())
print('\n', '__ne__', abc.__ne__())
print('\n', '__new__', abc.__new__())
print('\n', '__reduce__', abc.__reduce__())
print('\n', '__reduce_ex__', abc.__reduce_ex__())
print('\n', '__repr__', abc.__repr__())
print('\n', '__setattr__', abc.__setattr__())
print('\n', '__setstate__', abc.__setstate__())
print('\n', '__sizeof__', abc.__sizeof__())
print('\n', '__str__', abc.__str__())
print('\n', '__subclasshook__', abc.__subclasshook__())




from functools import partial

def foo(bar, baz):
    return bar + baz

empty_partial = partial(foo)
partial_partial = partial(empty_partial, bar=3)
full_partial = partial(partial_partial, baz=5)

print(full_partial())

# https://stackoverflow.com/questions/53201023/how-to-tell-if-a-partial-has-all-arguments-satisfied?noredirect=1#comment93290947_53201023
# how to tell if a partial has all arguments satisfied
# I don't believe partial exposes any well documented API to interrogate its func argument, so, generally, no. But you can certainly take the signature of func before you encapsulate it in partial and test the arguments against that signature. So, you'd have to write your own data structure/class around this to track the necessary information, partial probably doesn't give you what you need here

# for now I'll just put it in a try except clause, that'll be easy. try to run it, if success return result, if failure, yeild until given a new argument to add.
