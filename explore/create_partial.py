from functools import partial

def function_c(function_a, function_b):
    return function_a + function_b

def build_function_call(partial_function, arg=None):
    if arg:
        return partial(partial_function, **arg)
    return partial(partial_function)

# we have recieved a request on id 87 to run a function, but we need arguments first.
id = 87

# initially make the partial
function_call = build_function_call(function_c)

# each coroutine is added to a list of coroutines on the actor object
active_function_builds = {}
active_function_builds[id] = function_call

# simulate getting messages in for loop - this is what we'd do once we find the corresponding id in active_function_builds
ref_id = id
functions = ['function_a', 'function_b']
values = [3, 30]
for f, v in zip(functions, values):
    active_function_builds[ref_id] = build_function_call(active_function_builds[ref_id], {f: v})
    try:
        answer = active_function_builds[ref_id]()
    except Exception as e:
        pass

# this is where you would wrap this data in a message and send it back
print('ref_id', ref_id, 'response', answer)

del active_function_builds[ref_id]

print(active_function_builds)
