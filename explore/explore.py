GLOBAL_VARIABLE = 0

def first_try():
    def watch_global():
        ''' if GLOBAL_VARIABLE changes print out a message
            run forever without blocking the rest of the program. '''

        previous_GV = ''
        while True:
            if previous_GV != GLOBAL_VARIABLE:
                print('it was:', previous_GV , 'it now is:', GLOBAL_VARIABLE)
            previous_GV = GLOBAL_VARIABLE
            yield

    watch_global()
    # should print 'it was: '' it now is: 0

    print('doing other stuff')

    GLOBAL_VARIABLE += 1
    # should print 'it was: 0 it now is: 1

    print('doing other stuff')

#def second_try():

from threading import Thread
import time
GLOBAL_VARIABLE = 0

def watch_globals():
    print('watcher has started')
    global GLOBAL_VARIABLE       # Optional if you treat a as read-only
    previous_GV = ''
    while True:
        if previous_GV != GLOBAL_VARIABLE:
            print('it was:', previous_GV , 'it now is:', GLOBAL_VARIABLE)
        previous_GV = GLOBAL_VARIABLE
        yield

watcher = Thread(target=watch_globals)
watcher.start()
#watcher.join()

print('doing other stuff')
GLOBAL_VARIABLE += 1
# should print 'it was: 0 it now is: 1
print('doing other stuff')
GLOBAL_VARIABLE += 1
# should print 'it was: 0 it now is: 1
print('doing other stuff')
