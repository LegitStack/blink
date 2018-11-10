from message_board import MSGBoard
from node import Actor

def foo(bar, baz):
    return bar + baz

def get_self():
    import inspect
    frame_infos = inspect.stack()
    frame = frame_infos[1].frame
    locs = frame.f_locals
    return locs['self']

def bar(get_self):
    print('able to get information about the Actor: verbose is', get_self.verbose)
    return 3


def baz():
    return 30


def show(foo):
    print(foo)
    return True

# these function details could be deduced from their signature instead of made explicit...
actor_foo = Actor(verbose=True, functions={
    'foo': (foo, ('bar', 'baz')),
})
actor_bar = Actor(verbose=True, functions={
    'bar': (bar, ('get_self',)),
    'get_self': (get_self, tuple()),
})
actor_baz = Actor(verbose=True, functions={
    'baz': (baz, tuple()),
})
actor_user = Actor(verbose=True, functions={
    'show': (show, ('foo',)),
})

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts)
actor_bar.listen(thoughts)
actor_baz.listen(thoughts)
actor_user.listen(thoughts)

new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show'}

actor_user.say(message, thoughts)
