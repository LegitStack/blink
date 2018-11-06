import os
import sys
sys.path.append(os.getcwd())  # run from blink/
from message_board import MSGBoard


def test_add_message():
    board = MSGBoard('board')
    board.add_message('foo')
    assert board.messages == ['foo']


def test_read_message():
    board = MSGBoard('board')
    board.add_message('foo')
    assert board.get_message() == 'foo'


def test_read_messages():
    board = MSGBoard('board')
    board.add_message('foo')
    board.add_message('bar')
    board.add_message('baz')
    assert board.get_messages() == ['bar', 'baz']
