def test_function_0():
    print(f'test_function_0 :', 1)
    return 1


def test_function_1(test_function_2=1):
    print(f'test_function_1 : test_function_2={test_function_2}')
    return test_function_2


def test_function_2(test_function_3=1, test_function_4=2):
    print(f'test_function_2 : test_function_3={test_function_3}, arg2b={test_function_4}')
    return test_function_3 + test_function_4


def test_function_3(test_function_4=1):
    print(f'test_function_3 : test_function_4={test_function_4}')
    return test_function_4


def test_function_4(test_function_0=1):
    print(f'test_function_4 : test_function_0={test_function_0}')
    return test_function_0


def test_function_5(test_function_1=1, test_function_3=2):
    print(f'test_function_5 : test_function_1={test_function_1}, test_function_3={test_function_3}')
    return test_function_1 + test_function_3
