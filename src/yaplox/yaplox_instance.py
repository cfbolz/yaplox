from rpython.rlib import jit
from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError
from yaplox.obj import W_Root

class HiddenClass(object):
    def __init__(self):
        self.layout = {} # instance attribute names -> positions in storage
        self.next = {}

    @jit.elidable
    def lookup_position(self, name):
        return self.layout.get(name, -1)

    @jit.elidable
    def add_field(self, name):
        if name in self.next:
            return self.next[name]
        res = HiddenClass()
        res.layout = self.layout.copy()
        res.layout[name] = len(self.layout)
        self.next[name] = res
        return res

EMPTY = HiddenClass()

class YaploxInstance(W_Root):
    _immutable_fields_ = ['klass']

    def __init__(self, klass ):
        self.klass = klass
        self.hiddenclass = EMPTY
        self.storage = []

    def __repr__(self)  :
        return "%s instance" % (self.klass.name, )

    def get(self, name):
        pos = jit.promote(self.hiddenclass).lookup_position(name.lexeme)
        if pos >= 0:
            return self.storage[pos]

        jit.promote(self.klass)
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise YaploxRuntimeError(name, "Undefined property '%s'." % (name.lexeme, ))

    def set(self, name , value ):
        pos = jit.promote(self.hiddenclass).lookup_position(name.lexeme)
        if pos >= 0:
            self.storage[pos] = value
            return
        else:
            self.storage = self.storage + [value]
            self.hiddenclass = self.hiddenclass.add_field(name.lexeme)



