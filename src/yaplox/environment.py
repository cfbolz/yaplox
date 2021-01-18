from rpython.rlib import jit

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError
from yaplox.obj import W_Root, W_Number

class Cell(W_Root):
    def unwrap_cell(self):
        raise NotImplementedError("abstract base")

class ObjectCell(Cell):
    def __init__(self, value):
        self.value = value

    def unwrap_cell(self):
        return self.w_value


class NumCell(Cell):
    def __init__(self, numvalue):
        self.numvalue = numvalue

    def unwrap_cell(self):
        return W_Number(self.numvalue)


def write_cell(w_cell, w_value):
    if w_cell is None:
        # attribute does not exist at all, write it without a cell first
        return w_value
    if isinstance(w_cell, ObjectCell):
        w_cell.w_value = w_value
        return None
    elif isinstance(w_cell, NumCell) and type(w_value) is W_Number:
        w_cell.numvalue = w_value.num
        return None
    if type(w_value) is W_Number:
        return NumCell(w_value.num)
    else:
        return ObjectCell(w_value)


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
            return val.unwrap_cell()
        else:
            return val

    @jit.elidable
    def _get(self, name, version):
        return self.globals.get(name)

    def assign(self, name, w_val):
        oldval = self._get(name, jit.promote(self.version))
        newval = write_cell(oldval, w_val)
        if newval is None:
            return # written via cell
        self.globals[name] = newval
        self.version += 1

    define = assign


