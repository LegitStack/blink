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


def get_actor():
    frame_infos = inspect.stack()  # A list of FrameInfo.
    frame = frame_infos[1].frame   # The frame of the caller.
    locs = frame.f_locals          # The caller's locals dict.
    return locs['self']


def change_msg_board(get_actor, get_second_msg_board):
    get_actor.set_messageboard(get_second_msg_board.name)

def get_second_msg_board(get_actor):
    return get_actor.msgboards[1]

def print_something(get_second_msg_board):
    print(get_second_msg_board.name)
    return get_second_msg_board


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
words = MSGBoard('words')

actor_foo.listen(thoughts)
actor_kay.listen(thoughts)
actor_user.listen(thoughts)
actor_user.listen(words)

actor_user.add_function(function=show)
actor_user.add_function(function=shutdown)
actor_user.add_function(function=get_actor)
actor_user.add_function(function=change_msg_board)
actor_user.add_function(function=get_second_msg_board)
actor_user.add_function(function=print_something)
actor_foo.add_functions(functions=[foo, baz, shutdown])
actor_kay.add_functions(functions=[bar, kay, jay, nay, shutdown])
actor_user.add_trigger(cause='show', effect='nay')
