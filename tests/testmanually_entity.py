import sys
sys.path.append(os.getcwd())  # run from blink/
from node import Entity
from message_board import MSGBoard
import time

def create_basic_entity():
    def print_test():
        return 'hello_world'
    return Entity({
        'print_test': (print_test, ((),)),
        'print': (print, ('print_test',)),
        })


def test_listen():
    board = MSGBoard('board')
    a = create_basic_entity()
    b = create_basic_entity()
    b.listen(board)
    a.say('print_test', board)
    print(board.messages)
    time.sleep(2)
    a.say('print', board)
    time.sleep(2)
    a.say('print_test', board)
    time.sleep(2)
    a.say('print', board)
    time.sleep(2)
    a.say('print_test', board)
    time.sleep(2)
    print(board.messages)



test_listen()
