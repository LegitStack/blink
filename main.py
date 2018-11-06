from message_board import MSGBoard
from node import Entity


def test_function_1(arg1=1):
    print(f'test_function_1 : arg1={arg1}')
    return arg1


def test_function_2(arg1=1, arg2=2):
    print(f'test_function_2 : arg1={arg1}, arg2={arg2}')
    return arg1 + arg2


def test_function_3(arg1=1, arg2=2, arg3=3):
    print(f'test_function_3 : arg1={arg1}, arg2={arg2}, arg3={arg3}')
    return arg1 + arg2 + arg3


def test_function_4(arg1=1, arg2=2, arg3=3, arg4=4):
    print(f'test_function_4 : arg1={arg1}, arg2={arg2}, arg3={arg3}, arg4={arg4}')
    return arg1 + arg2 + arg3 + arg4


def test_function_5(arg1=1, arg2=2, arg3=3, arg4=4, arg5=5):
    print(f'test_function_5 : arg1={arg1}, arg2={arg2}, arg3={arg3}, arg4={arg4}, arg5={arg5}')
    return arg1 + arg2 + arg3 + arg4 + arg5


thoughts = MSGBoard('thoughts')
words = MSGBoard('words')
deeds = MSGBoard('deeds')


a = Entity({
    'test_function_1': (test_function_1, ('arg1',))
    })
b = Entity({
    'test_function_2': (test_function_2, ('arg1', 'arg2',)),
    'test_function_3': (test_function_3, ('arg1', 'arg2', 'arg3',))
    })
c = Entity({
    'test_function_4': (test_function_4, ('arg1', 'arg2', 'arg3', 'arg4',)),
    'test_function_5': (test_function_5, ('arg1', 'arg2', 'arg3', 'arg4', 'arg5',))
    })
