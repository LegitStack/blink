from functools import partial

def function_c(function_a, function_b):
    return function_a + function_b

def build_function_call(id, function):
    args = {}
    print('coroutine started')
    still_partial = True
    while still_partial:
        new_argument = yield
        args[new_argument[0]] = new_argument[1]
        try:
            answer = function(**args)
            still_partial = False
            yield id, answer
        except Exception as e:
            pass
    print('exiting coroutine')



# we have recieved a request on id 87 to run a function, but we need arguments first.
id = 87

# initially make the coroutine
function_call = build_function_call(id, function_c)
next(function_call)

# each coroutine is added to a list of coroutines on the actor object
active_function_builds = {}
active_function_builds[id] = function_call

# simulate getting messages in for loop - this is what we'd do once we find the corresponding id in active_function_builds
ref_id = id
functions = ['function_a', 'function_b']
values = [3, 30]
for f, v in zip(functions, values):
    answer = active_function_builds[ref_id].send((f, v))
    if answer:
        break

# this is where you would wrap this data in a message and send it back
print('ref_id', answer[0], 'response', answer[1])

# clear out that coroutine
try:
    next(function_call)
except Exception as e:
    del active_function_builds[ref_id]


print(active_function_builds)
