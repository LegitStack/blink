import sys
from threading import Thread
from functools import partial
from inspect import signature

# TODO add ability to refer to a different board,
# TODO add ability to trigger messages to go to a different board.
# TODO add ability for user to talk to actor who asks for things.

class Actor():
    ''' an entity does computation, though nobody else knows what it is or how to call it. '''

    def __init__(self, functions: dict, verbose=False):
        ''' functions is a dictionary:
            {name: (function, arguments)}
            {string: (function, tuple of function names)}
            feel free wrap state in functions. '''
        self.functions = functions
        self.msgboards = []
        self.partial_builds = {}
        self.verbose = verbose

    def listen(self, msgboard, debug=False):

        def wire(msgboard):
            print(f'listening to {msgboard.name} forever') if self.verbose else None
            seen_messages = []
            if debug:
                import time
                t_end = time.time() + 6
                condition = 'time.time() < t_end'
            else:
                condition = 'True'
            while eval(condition):
                all_messages = msgboard.get_messages(0)
                all_ids = [msg['id'] for msg in all_messages]
                missing_ids = sorted(set(all_ids) - set(seen_messages))
                for missing_id in missing_ids:
                    message = [msg for msg in all_messages if msg['id'] == missing_id][0]
                    self.new_message_trigger(message, msgboard)
                    seen_messages.append(missing_id)

        threads = []
        threads.append(Thread(target=wire, args=(msgboard,)))

        try:
            threads[-1].start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        self.msgboards.append(msgboard)

        print('saved', self.msgboards) if self.verbose else None

    def new_message_trigger(self, message, msgboard):
        '''
        determin if we care about this message or not:
        if message is a request for one of it's functions, do the function
            requests include id, ref_id, request (the name of a function)
        if message is a response, see if it's a response to a request you made
            responses include id, ref_id, request, response (data (could be function name...))
        if message is a behavior someone else did, see if it should trigger a function
        # elif msgboard.name == 'behavior':
        #     self.handle_behavior(message, msgboard)
        # else:
        #     self.handle_unknown(message, msgboard)
        '''
        if 'response' not in message.keys():
            self.handle_request(message=message, msgboard=msgboard)
        elif 'response' in message.keys():
            self.handle_response(message=message, msgboard=msgboard)

    def manage_substituion(self, message, argument):
        '''
        if a message is a request a substitution for an argument may be included
        in the form of the name of a different function. it looks like this:
        {'id': 1, 'ref_id': 1, 'request': 'foo', 'substitutions': {'bar': 'baz', 'baz': 'bar'}}
        we want this functionality: foo(bar=bar, baz=baz) -> foo(bar=baz, baz=bar)
        thus when I see substitution and I need to ask for functions, I really need
        to ask for the substituted functions names, and I should check if I own the
        substituted names rather than the originals.
        '''
        if 'substitutions' not in message.keys() and 'substitution' not in message.keys():
            substitution = None
        elif 'substitution' in message.keys():
            substitution = message['substitution']
        else:
            substitution = argument

        if 'substitutions' in message.keys():
            if argument in message['substitutions'].keys():
                return message['substitutions'][argument], substitution
        return argument, substitution


    def handle_request(self, message, msgboard):
        '''
        search for the function, if I don't have it ignore, if I do, run it
        # initially make the partial
        # each coroutine is added to a list of coroutines on the actor object
        # ask for all the arguments for this function
        # let go of control
        '''
        if message['request'] in self.functions.keys():
            print('incoming request', message) if self.verbose else None
            function, arguments = self.functions[message['request']]
            function_call = self.build_partial(function)
            self.partial_builds[message['id']] = message['request'], function_call, message['ref_id']
            if not self.attempt(
                ref_id=message['id'],
                message=message,
                msgboard=msgboard,
            ):
                for argument in arguments:
                    arg, substitution = self.manage_substituion(message, argument)
                    request_message = self.craft_message(
                        ref_id=message['id'],
                        msgboard=msgboard,
                        request=arg,
                        substitution=substitution,
                    )
                    self.say(message=request_message, msgboard=msgboard)

    def handle_response(self, message, msgboard):
        '''
        search my history to see if I made the request, if so continue running that function.
        # add argument from message to partial function,
        # try to run, if success return results.
        # let go of control
        '''
        if message['ref_id'] in self.partial_builds.keys():
            print('incoming response', message) if self.verbose else None
            ref_id = message['ref_id']
            if ('substitution' in message
            and message['substitution'] in list(signature(self.partial_builds[ref_id][1]).parameters)):
                arg = message['substitution']
            else:
                arg = message['request']
            self.partial_builds[ref_id] = self.partial_builds[ref_id][0], self.build_partial(
                partial_function=self.partial_builds[ref_id][1],
                argument={arg: message['response']}
            ), self.partial_builds[ref_id][2]
            self.attempt(
                ref_id=ref_id,
                message=message,
                msgboard=msgboard,
            )

    def build_partial(self, partial_function, argument=None):
        ''' turn function into partial or add arguments to existing partial '''
        if argument:
            return partial(partial_function, **argument)
        return partial(partial_function)

    def attempt(self, ref_id, message, msgboard):
        success, response = self.try_to_run(self.partial_builds[ref_id][1])
        if success:
            message = self.craft_response(
                message=message,
                msgboard=msgboard,
                ref_id=self.partial_builds[ref_id][2],
                request=self.partial_builds[ref_id][0],
                response=response,
            )
            self.say(
                message=message,
                msgboard=msgboard,
            )
            del self.partial_builds[ref_id]
            return True
        return False

    def try_to_run(self, function):
        try:
            response = function()
            return True, response
        except Exception as e:
            return False, None

    def craft_response(self, message, msgboard, ref_id=None, request=None, response=None):
        ref_id = ref_id or message['id']
        if 'substitution' in message.keys():
            substitution = message['substitution']
        else:
            substitution = None
        return self.craft_message(
            msgboard=msgboard,
            ref_id=ref_id,
            response=response,
            request=request,
            substitution=substitution,
        )

    def craft_message(
        self,
        msgboard,
        ref_id=None,
        response=None,
        request=None,
        substitution=None,
        substitutions=None,
    ):
        message = {'id': msgboard.produce_id()}
        if ref_id:
            message['ref_id'] = ref_id
        if response:
            message['response'] = response
        if request:
            message['request'] = request
        if substitution:
            message['substitution'] = substitution
        if substitutions:
            message['substitutions'] = substitutions
        return message

    def say(self, message, msgboard):
        print('outgoing message', message) if self.verbose else None
        msgboard.add_message(message)
