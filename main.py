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


def show_bar(bar):
    print(bar)


def show_baz(baz):
    print(baz)


def show_foo(foo):
    print(foo)
    return True


actor_foo = Actor(functions={
    'foo': (foo, ('bar', 'baz', 'nay')),
})
actor_bar = Actor(functions={
    'bar': (bar, tuple()),
})
actor_baz = Actor(functions={
    'baz': (baz, tuple()),
})
actor_kay = Actor(functions={
    'kay': (kay, tuple()),
})
actor_jay = Actor(functions={
    'jay': (jay, tuple()),
})
actor_nay = Actor(functions={
    'nay': (nay, ('kay', 'jay')),
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
actor_kay.listen(thoughts)
actor_jay.listen(thoughts)
actor_nay.listen(thoughts)
actor_user.listen(thoughts)
new_id = thoughts.produce_id()
message = {'id': new_id, 'ref_id': new_id, 'request': 'show_foo'}

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
