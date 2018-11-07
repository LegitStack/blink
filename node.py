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
        self.msgboards = []

    def listen(self, msgboard):
        import time
        def wire(msgboard):
            print(f'listening to {msgboard.name} forever')
            previous_id = ''
            #while True:
            for i in range(15):
                time.sleep(1)
                latest_message = msgboard.get_message()
                if previous_id != latest_message['id']:
                    print('found new message', latest_message)
                    new_message_trigger(latest_message, msgboard.name)
                    previous_id = latest_message['id']
                print(i)

        threads = []
        threads.append(Thread(target=wire, args=(msgboard,)))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        self.msgboards.append(msgboard)

    def new_message_trigger(self, message, msgboard):
        '''
        determin if we care about this message or not:
        if message is a request for one of it's functions, do the function
        if message is a response, see if it's a response to a request you made
        if message is a behavior someone else did, see if it should trigger a function
        '''
        if msgboard.name == 'request':
            self.handle_request(message, msgboard)
        elif msgboard.name == 'response':
            self.handle_response(message, msgboard)
        elif msgboard.name == 'behavior':
            self.handle_behavior(message, msgboard)
        else:
            self.handle_unknown(message, msgboard)

    def handle_request(self, message, msgboard):
        '''
        search for the function, if I don't have it ignore, if I do, run it
        '''
        if self.search(message['function']):
            response = self.run_function(message['function'])
            message = self.produce_message(
                msgboard=msgboard,
                ref_id=message['id'],
                ref_board=msgboard.name,
                response=response)
            response_board = get_message_board(name='response')
            self.say(message, response_board)

    def handle_response(self, message, msgboard):
        '''
        search my history to see if I made the request, if so continue running that function.
        '''
        if self.search_history(message['request_id']):
            pass
            # return to the coroutine that is working on runing that function.
            # if this repsonse gives that coroutine everything it needs then it will run the function,
            # if it's still waiting on stuff it'll update the partial and yeild.

    def handle_behavior(self, message, msgboard):
        '''
        search for a trigger for that behavior, if I have one, run the function
        '''
        trigger, function = self.search_triggers(message['behavior'])
        if trigger:
            self.run_function(function)

    def handle_unknown(self, message, msgboard):
        '''
        search for the function, if I don't have it ignore, if I do, run it
        '''
        if 'function' in message.keys():
            if self.search(message['function']):
                self.run_function(message['function'])

    def search(self, name):
        if name in self.functions.keys():
            return self.functions[name]

    def produce_message(self, ref_id=None, response=None, function=None):
        message = {}
        if ref_id:
            message['ref_id'] = ref_id
        if response:
            message['response'] = response
        if function:
            message['function'] = function
        return message

    def run_function(self, name):
        '''
        this should be a coroutine that yeilds when it doesn't have all the args
        once it has all the args it should terminate, and be removed from the list of currently waiting coroutines.
        if the entity does have all the inputs, return the result of the function.
        if the entity is missing one or more inputs, ask for them.
        '''
        function, arguments = self.functions[name]
        # if this function requires no args
        if arguments == (,):
            return self.functions[name][0]()
        # elif I already have all the args then each of those are functions...
        # so run those and get the results and return the results to the
        # argument list and return the reults of the ran function:
        else:
            # do I have all the functions that are the arguments?
            # return self.functions[name][0]()
            pass
        # yeild somewhere...

    def get_message_board(self, name):
        for board in self.msgboards:
            if board.name == name:
                return board

    def say(self, message, msgboard):
        msgboard.add_message(message)

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


    def search_supplied(self, name, supplied: dict = None):
        supplied = supplied or {}
        if name in supplied:
            return supplied[name]

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



#'''
#for now this is for testing purposes
#msgboard is a message_board.MSGBoard object
