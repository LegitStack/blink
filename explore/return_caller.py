import inspect

#def baz():
    # return the object instance that calls me.
    # print(inspect.stack())
#    return inspect.stack() #[1][3]
def baz(s):
    return s


class Foo():
    def bar(self, func):
        return func(self)  # should return the Foo object but how???

    def moo(self):
        print('moo')

new_foo = Foo()
print(new_foo)

new_foo_instance = new_foo.bar(baz)
print(new_foo_instance)

new_foo.moo()
new_foo_instance.moo()
