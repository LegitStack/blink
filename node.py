import sys
from threading import Thread
from functools import partial

# TODO: add in subsitutes to the protocol because we need to be able to substitute one argument for a different function


class Actor():
    ''' an entity does computation, though nobody else knows what it is or how to call it. '''

    def __init__(self, functions: dict):
        ''' functions is a dictionary:
            {name: (function, arguments)}
            {string: (function, tuple of function names)}
            feel free wrap state in functions. '''
        self.functions = functions
        self.msgboards = []
        self.partial_builds = {}
        self.partial_build_requests = {}
        # key is id of request sent out,
        # value is tuple:
        #   (name of argument function originally requested,
        #   partial function of the original function that I own)

    def listen(self, msgboard):
        import time

        def wire(msgboard):
            print(f'listening to {msgboard.name} forever')
            seen_messages = []
            # while True:
            for i in range(10):
                time.sleep(1)
                all_messages = msgboard.get_messages(0)  # get all messages
                all_ids = [msg['id'] for msg in all_messages]
                missing_ids = sorted(set(all_ids) - set(seen_messages))  # oldest to newest
                for missing_id in missing_ids:
                    message = [msg for msg in all_messages if msg['id'] == missing_id][0]
                    print('found new message', message)
                    self.new_message_trigger(message, msgboard)
                    seen_messages.append(missing_id)
                print(i)

        threads = []
        threads.append(Thread(target=wire, args=(msgboard,)))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        self.msgboards.append(msgboard)

        print('saved', self.msgboards)

    def new_message_trigger(self, message, msgboard):
        '''
        determin if we care about this message or not:
        if message is a request for one of it's functions, do the function
        if message is a response, see if it's a response to a request you made
        if message is a behavior someone else did, see if it should trigger a function
        '''
        # right now the type of message is determined by the message itself.
        # we can, however, in the future make boards for requests and responses
        # right now we're assuming one message board to reduce complexity.
        # in this model each board might be centered around a topic or something.
        if 'response' not in message.keys():
            self.handle_request(message=message, msgboard=msgboard)
            # requests include id, ref_id, request (the name of a function)
        elif 'response' in message.keys():
            self.handle_response(message=message, msgboard=msgboard)
            # responses include id, ref_id, request, response (data (could be function name...))
        # elif msgboard.name == 'behavior':
        #     self.handle_behavior(message, msgboard)
        # else:
        #     self.handle_unknown(message, msgboard)

    def handle_request(self, message, msgboard):
        ''' search for the function, if I don't have it ignore, if I do, run it '''
        if message['request'] in self.functions.keys():
            function, arguments = self.functions[message['request']]
            # initially make the partial
            function_call = self.build_partial(function)
            # each coroutine is added to a list of coroutines on the actor object
            self.partial_builds[message['id']] = message['request'], function_call
            if not self.attempt(ref_id=message['id'], message=message, msgboard=msgboard):
                # ask for all the arguments for this function
                for argument in arguments:
                    request_message = self.craft_message(
                        message=message,
                        ref_id=message['id'],
                        msgboard=msgboard,
                        request=argument,
                    )
                    self.say(message=request_message, msgboard=msgboard)
                    self.partial_build_requests[request_message['id']] = message['id']
        # let go of control

    def handle_response(self, message, msgboard):
        ''' search my history to see if I made the request, if so continue running that function. '''
        if message['ref_id'] in self.partial_build_requests.keys():
            print('I have been waiting for ', message)
            ref_id = self.partial_build_requests[message['ref_id']]
            print('I have been waiting!!!', ref_id)
            print('-//', self.partial_build_requests)  # HERE WE":RE MISSING WHAT WE SHOULD GIVE BACK TO. conection for 1-2
            # add argument from message to partial function, try to run, if success return results.
            self.partial_builds[ref_id] = self.partial_builds[ref_id][0], self.build_partial(
                partial_function=self.partial_builds[ref_id][1],
                argument={message['request']: message['response']}
            )
            print('partial_builds', self.partial_builds)
            self.attempt(
                ref_id=ref_id,
                message=message,
                msgboard=msgboard,
            )
        # let go of control

    def build_partial(self, partial_function, argument=None):
        ''' turn function into partial or add arguments to existing partial '''
        if argument:
            return partial(partial_function, **argument)
        return partial(partial_function)

    def attempt(self, ref_id, message, msgboard):
        response = self.try_to_run(ref_id, self.partial_builds[ref_id][1])
        print('---', response)
        if response:
            message = self.craft_response(
                message=message,
                msgboard=msgboard,
                request=self.partial_builds[ref_id][0],
                response=response,
            )
            print(message)
            self.say(
                message=message,
                msgboard=msgboard,
            )
            del self.partial_builds[ref_id]
            return True
        return False

    def try_to_run(self, ref_id, function):
        try:
            response = function()
            return response
        except Exception as e:
            return None

    def craft_response(self, message, msgboard, request=None, response=None):
        ref_id = message['id']
        return self.craft_message(
            message=message,
            msgboard=msgboard,
            ref_id=ref_id,
            response=response,
            request=request,
        )

    def craft_message(self, message, msgboard, ref_id=None, response=None, request=None):
        message = {}
        message['id'] = msgboard.produce_id()
        if ref_id:
            message['ref_id'] = ref_id
        if response:
            message['response'] = response
        if request:
            message['request'] = request
        return message

    def say(self, message, msgboard):
        msgboard.add_message(message)


# ##############################################################################
# obsolite?
# ##############################################################################
#
#    def run_function(self, name):
#        '''
#        this should be a coroutine that yeilds when it doesn't have all the args
#        once it has all the args it should terminate, and be removed from the list of currently waiting coroutines.
#        if the entity does have all the inputs, return the result of the function.
#        if the entity is missing one or more inputs, ask for them.
#        You'll probably need a 'partial maker coroutine' then add each coroutine object to a queue to look at later.
#        '''
#        function, arguments = self.functions[name]
#        # if this function requires no args
#        if len(arguments) == 0:  # == (, )
#            return self.functions[name][0]()
#        # elif I already have all the args then each of those are functions...
#        # so run those and get the results and return the results to the
#        # argument list and return the reults of the ran function:
#        else:
#            # do I have all the functions that are the arguments?
#            # return self.functions[name][0]()
#            pass
#        # yeild somewhere...
#
#    def get_missing_function_reqs(self, name):
#        search_result = self.search(name)
#
#        if search_result:  # we have the function
#            for req in search_result[1]:
#                print(req, self.search(req))
#            return [req for req in search_result[1] if self.search(req) is None]
#
#    def act(self, name):
#        pass
#        # # talk this through, it's not right
#        # arguments = self.functions[name][1]
#        # for argument in arguments:
#        #     search_result = self.search(argument)
#        #     if search_result:  # we have the function
#        #         d_arg = {argument: self.act(search_result)}
#        #         # m1 = partial(mult, y=2)
#        #         # print(m1(x=3))
#
#    def search_supplied(self, name, supplied: dict = None):
#        supplied = supplied or {}
#        if name in supplied:
#            return supplied[name]
#
#        # def hear(self, msgboard):
#        #     def listen(msgboard):
#        #         print(f'listening to {msgboard.name} forever')
#        #         previous_message = ''
#        #         while True:
#        #             latest_message = msgboard.get_message()
#        #             if previous_message != latest_message:
#        #                 print('should we do something about this?', latest_message)
#        #             previous_message = latest_message
#        #             yield
#        #     while True:
#        #         b.listen()
#
#



### reduce complexity, add these in later:


# def handle_behavior(self, message, msgboard):
#     '''
#     search for a trigger for that behavior, if I have one, run the function
#     '''
#     trigger, function = self.search_triggers(message['behavior'])
#     if trigger:
#         self.run_function(function)

# def handle_unknown(self, message, msgboard):
#     '''
#     search for the function, if I don't have it ignore, if I do, run it
#     '''
#     if 'function' in message.keys():
#         if self.search(message['request']):
#             self.run_function(message['request'])
