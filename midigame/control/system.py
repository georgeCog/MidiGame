import random
import time
import keyboard
from functools import wraps

def delay(func):
    @wraps(func)
    def delayed_func(*args, **kwargs):
        time.sleep(random.uniform(0, 0.1))
        func(*args, **kwargs)
    return delayed_func

class SystemController:
    def __init__(self):
        pass
    @delay
    def press(self, key):
        keyboard.press(key)
    @delay
    def release(self, key):
        keyboard.release(key)
    def get_presser(self, key):
        def func():
            self.press(key)
        return func
    def get_releaser(self, key):
        def func():
            self.release(key)
        return func