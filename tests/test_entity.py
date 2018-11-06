import os
import sys
sys.path.append(os.getcwd())  # run from blink/
from node import Entity
from message_board import MSGBoard


def create_basic_entity():
    def print_test():
        return 'hello_world'
    return Entity({
        'print_test': (print_test, ((),)),
        'print': (print, ('print_test',)),
        })


def create_complex_entity():
    def print_test():
        return 'hello_world'
    return Entity({
        'print_test': (print_test, ('missing_function',)),
        'print': (print, ('print_test',)),
        })


def test_creation():
    entity = Entity({
        'print': (print, ((),)),
        })
    assert entity is not None


def test_search_missing():
    assert create_basic_entity().search('test') is None


def test_search_find():
    assert create_basic_entity().search('print_test') is not None


def test_say():
    board = MSGBoard('board')
    entity = create_basic_entity()
    entity.say('print_test', board)
    assert board.messages == ['hello_world']


def test_find_reqs_empty():
    assert create_basic_entity().get_missing_function_reqs('print_test') == [()]


#def test_find_reqs_full():
#    assert create_complex_entity().get_missing_function_reqs('print') == ('print_test',)
#
#create_complex_entity().get_missing_function_reqs('print_test')
