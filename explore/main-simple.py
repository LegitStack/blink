from message_board import MSGBoard
from node import Actor


def foo(bar, baz):
    return bar + baz


def bar():
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
    'bar': (bar, tuple()),
})
actor_baz = Actor(verbose=True, functions={
    'baz': (baz, tuple()),
})
actor_user = Actor(verbose=True, functions={
    'show': (show, ('foo',)),
})

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts, debug=True)
actor_bar.listen(thoughts, debug=True)
actor_baz.listen(thoughts, debug=True)
actor_user.listen(thoughts,debug=True)

new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show'}

actor_user.say(message, thoughts)
