from threading import Lock

s_print_lock = Lock()

def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


def s_input(*a):
    """Thread safe input function"""
    with s_print_lock:
        print(*a, end='')
    return input('')

