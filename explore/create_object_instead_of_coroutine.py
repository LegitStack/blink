from functools import partial

def function_c(function_a, function_b):
    return function_a + function_b

def create_partial(id, function):
    args = {}
    print('coroutine started')
    still_partial = True
    while still_partial:
        print('y')
        new_argument = yield
        args[new_argument[0]] = new_argument[1]
        print(args)
        try:
            answer = function(**args)
            print('id', id, 'answer', answer)
            #return id, answer
            yield answer
            yield answer
            print('yeilded')
        except Exception as e:
            pass



function_call = create_partial(87, function_c)
next(function_call)
function_call.send(('function_a',3))
function_call.send(('function_b',30))
import time
time.sleep(1)
answer = next(function_call)
print(answer)
#print(whatever, id)
