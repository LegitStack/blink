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
})
actor_bar = Actor(verbose=True, functions={
    'bar': (bar, tuple()),
})
actor_baz = Actor(verbose=True, functions={
    'baz': (baz, tuple()),
})
actor_kay = Actor(verbose=True, functions={
    'kay': (kay, tuple()),
})
actor_jay = Actor(verbose=True, functions={
    'jay': (jay, tuple()),
})
actor_nay = Actor(verbose=True, functions={
    'nay': (nay, ('kay', 'jay')),
})
actor_user = Actor(verbose=True, functions={
    'show': (show, ('foo',)),
})

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts)
actor_bar.listen(thoughts)
actor_baz.listen(thoughts)
actor_kay.listen(thoughts)
actor_jay.listen(thoughts)
actor_nay.listen(thoughts)
actor_user.listen(thoughts)

new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show', 'substitutions': {'foo':'nay'}}

actor_user.say(message, thoughts)
