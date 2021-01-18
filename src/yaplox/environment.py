from rpython.rlib import jit

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError
from yaplox.obj import W_Root

class Cell(W_Root):
    def __init__(self, value):
        self.value = value

class Globals(object):
    _immutable_fields_ = ['version?']
    def __init__(self):
        self.globals = {}
        self.version = 0

    def get(self, name):
        jit.promote(self)
        version = self.version
        jit.promote(version)
        val = self._get(name, version)
        if isinstance(val, Cell):
            return val.value
        else:
            return val

    @jit.elidable
    def _get(self, name, version):
        return self.globals.get(name)

    def assign(self, name, w_val):
        oldval = self._get(name, jit.promote(self.version))
        if oldval is None:
            self.globals[name] = w_val
            self.version += 1
        else:
            if isinstance(oldval, Cell):
                oldval.value = w_val
            else:
                self.globals[name] = Cell(w_val)
                self.version += 1

    define = assign


