from message_board import MSGBoard
from node import Entity
from functions import \
    test_function_0, test_function_1, test_function_2, test_function_3, test_function_4, test_function_5


thoughts = MSGBoard('thoughts')
words = MSGBoard('words')
deeds = MSGBoard('deeds')


a = Entity({
    'test_function_0': (test_function_0, (None,)),
    'test_function_1': (test_function_1, ('test_function_2',))
    })
b = Entity({
    'test_function_2': (test_function_2, ('test_function_3', 'test_function_4',)),
    'test_function_3': (test_function_3, ('test_function_4', ))
    })
c = Entity({
    'test_function_4': (test_function_4, ('test_function_0',)),
    'test_function_5': (test_function_5, ('test_function_1', 'test_function_3',))
    })
