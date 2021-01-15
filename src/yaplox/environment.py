
from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError

class Globals(object):
    def __init__(self):
        self.globals = {}


    def get(self, name):
        return self.globals.get(name)

    def assign(self, name, w_val):
        self.globals[name] = w_val
    define = assign


