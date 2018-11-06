from threading import Thread
import sys
# from functools import partial


class Entity():
    ''' an entity does computation, though nobody else knows what it is or how to call it. '''

    def __init__(self, functions: dict):
        ''' functions is a dictionary:
            {name: (function, arguments)}
            {string: (function, tuple of function names)}
            feel free wrap state in functions. '''
        self.functions = functions

    def get_missing_function_reqs(self, name):
        search_result = self.search(name)
        if search_result:  # we have the function
            for req in search_result[1]:
                print(req, self.search(req))
            return [req for req in search_result[1] if self.search(req) is None]

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
        ''' msgboard is a message_board.MSGBoard object '''
        msgboard.add_message(self.functions[name][0]())

    #def hear(self, msgboard):
    #    def listen(msgboard):
    #        print(f'listening to {msgboard.name} forever')
    #        previous_message = ''
    #        while True:
    #            latest_message = msgboard.get_message()
    #            if previous_message != latest_message:
    #                print('should we do something about this?', latest_message)
    #            previous_message = latest_message
    #            yield
    #    while True:
    #        b.listen()

    def listen(self, msgboard):
        import time
        def wire(msgboard):
            print(f'listening to {msgboard.name} forever')
            previous_message = ''
            #while True:
            for i in range(15):
                time.sleep(1)
                latest_message = msgboard.get_message()
                if previous_message != latest_message:
                    print('should we do something about this?', latest_message)
                    previous_message = latest_message
                print(i)

        threads = []
        threads.append(Thread(target=wire, args=(msgboard,)))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        threads[-1].join()

    def search(self, name):
        if name in self.functions.keys():
            return self.functions[name]

    def search_supplied(self, name, supplied: dict = None):
        supplied = supplied or {}
        if name in supplied:
            return supplied[name]
