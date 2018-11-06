# from functools import partial


class Entity():
    ''' an entity does computation, though nobody else knows what it is or how to call it. '''

    def __init__(self, functions: dict):
        ''' functions is a dictionary:
            {name: (function, arguments)}
            {string: (function, tuple of function names)}
            feel free wrap state in functions. '''
        self.functions = functions

    def act(self, name):
        pass
        # # talk this through, it's not right
        # arguments = self.functions[name][1]
        # for argument in arguments:
        #     search_result = self.search(argument)
        #     if search_result:  # we have the function
        #         d_arg = {argument: self.act(search_result)}
        #         # m1 = partial(mult, y=2)
        #         # print(m1(x=3))

    def say(self, name, msgboard):
        msgboard.add_message(self.functions[name])

    def listen(self, msgboard):
        pass
        # msgboard

    def search(self, name):
        if name in self.functions.keys():
            return self.functions[name]
