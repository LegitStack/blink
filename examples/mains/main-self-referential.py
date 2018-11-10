from message_board import MSGBoard
from node import Actor


def foo(bar, baz, nay):
    return bar + baz + nay


def bar():
    return 3


def baz():
    return 30


def kay():
    return 300


def jay():
    return 3000


def nay(kay, jay):
    return kay + jay


def show(foo):
    print(foo)
    return True

# these function details could be deduced from their signature instead of made explicit...
actor_foo = Actor(verbose=True, functions={
    'foo': (foo, ('bar', 'baz', 'nay')),
    'baz': (baz, tuple()),
})
actor_kay = Actor(verbose=True, functions={
    'bar': (bar, tuple()),
    'kay': (kay, tuple()),
    'jay': (jay, tuple()),
})
actor_user = Actor(verbose=True, functions={
    'show': (show, ('foo',)),
    'nay': (nay, ('kay', 'jay')),
})

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts)
actor_kay.listen(thoughts)
actor_user.listen(thoughts)

new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show'}

actor_user.say(message, thoughts)
