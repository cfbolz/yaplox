from rpython.rlib import jit
from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError
from yaplox.obj import W_Root


class YaploxInstance(W_Root):
    _immutable_fields_ = ['klass']

    def __init__(self, klass ):
        self.klass = klass
        self.fields = {}

    def __repr__(self)  :
        return "%s instance" % (self.klass.name, )

    def get(self, name):
        try:
            return self.fields[name.lexeme]
        except KeyError:
            pass

        jit.promote(self.klass)
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise YaploxRuntimeError(name, "Undefined property '%s'." % (name.lexeme, ))

    def set(self, name , value ):
        self.fields[name.lexeme] = value
