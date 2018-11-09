from message_board import MSGBoard
from node import Actor


def foo(bar, baz):
    return bar + baz


def bar():
    return 3


def baz():
    return 30


def show_bar(bar):
    print(bar)


def show_baz(baz):
    print(baz)


def show_foo(foo):
    print(foo)


actor_foo = Actor(functions={
    'foo': (foo, ('bar', 'baz')),
})
actor_bar = Actor(functions={
    'bar': (bar, tuple()),
})
actor_baz = Actor(functions={
    'baz': (baz, tuple()),
})
actor_user = Actor(functions={
    'show_bar': (show_bar, ('bar',)),
    'show_baz': (show_baz, ('baz',)),
    'show_foo': (show_foo, ('foo',)),
})

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts)
actor_bar.listen(thoughts)
actor_baz.listen(thoughts)
actor_user.listen(thoughts)
new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show_foo'}

import time
time.sleep(3)
actor_user.say(message, thoughts)

# thoughts = MSGBoard('thoughts')
# words = MSGBoard('words')
# deeds = MSGBoard('deeds')
#
# from functions import \
# test_function_0, test_function_1, test_function_2, test_function_3, test_function_4, test_function_5
#
# a = Entity({
#     'test_function_0': (test_function_0, (None,)),
#     'test_function_1': (test_function_1, ('test_function_2',))
#     })
# b = Entity({
#     'test_function_2': (test_function_2, ('test_function_3', 'test_function_4',)),
#     'test_function_3': (test_function_3, ('test_function_4', ))
#     })
# c = Entity({
#     'test_function_4': (test_function_4, ('test_function_0',)),
#     'test_function_5': (test_function_5, ('test_function_1', 'test_function_3',))
#     })
