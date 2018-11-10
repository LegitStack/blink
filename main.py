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


def shutdown():
    import sys
    print('shutting down')
    sys.exit()
    exit()


# def user_input():
#     import threading
#     import time
#     import sys
#
#     def background():
#         while True:
#             time.sleep(3)
#             print('disarm me by typing disarm')
#
#
#     def show_trigger():
#         .msgboards.append(msgboard)
#
#         new_id = thoughts.produce_id()
#         message = {'id': new_id, 'ref_id': new_id, 'request': 'show'}
#         actor_user.say(message, thoughts)
#
#     # now threading1 runs regardless of user input
#     threading1 = threading.Thread(target=background)
#     threading1.daemon = True
#     threading1.start()
#
#     while True:
#         if input() == 'disarm':
#             show_trigger()
#             sys.exit()
#         else:
#             print('not disarmed')




# these function details could be deduced from their signature instead of made explicit...
actor_foo = Actor(verbose=True)
actor_kay = Actor(verbose=True)
actor_user = Actor(accepts_user_input=True, verbose=True)

thoughts = MSGBoard('thoughts')

actor_foo.listen(thoughts)
actor_kay.listen(thoughts)
actor_user.listen(thoughts)

actor_foo.add_function(name='foo', function=foo, arguments=('bar', 'baz', 'nay'))
actor_foo.add_function(name='baz', function=baz, arguments=tuple())
actor_foo.add_function(name='shutdown', function=shutdown, arguments=tuple())
actor_kay.add_function(name='bar', function=bar, arguments=tuple())
actor_kay.add_function(name='kay', function=kay, arguments=tuple())
actor_kay.add_function(name='jay', function=jay, arguments=tuple())
actor_kay.add_function(name='nay', function=nay, arguments=('kay', 'jay'))
actor_kay.add_function(name='shutdown', function=shutdown, arguments=tuple())
actor_user.add_function(name='show', function=show, arguments=('foo',))
actor_user.add_function(name='shutdown', function=shutdown, arguments=tuple())
actor_user.add_trigger(name='show', function_name='shutdown')
