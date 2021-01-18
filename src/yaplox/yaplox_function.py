from rpython.rlib import jit

from yaplox.stmt import Function
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_instance import YaploxInstance
from yaplox.yaplox_return_exception import YaploxReturnException

entrydriver = jit.JitDriver(greens=['declaration'], reds=['subinterp', 'self'], should_unroll_one_iteration=lambda *args: True)

class YaploxFunction(YaploxCallable):
    _immutable_fields_ = ['closure', 'declaration', 'is_initializer']

    def __init__(
        self,
        declaration ,
        closure ,
        is_initializer ,
    ):
        YaploxCallable.__init__(self)
        self.closure = closure
        self.declaration = declaration
        self.is_initializer = is_initializer

    def bind(self, instance)  :
        jit.promote(self.declaration)
        interp = self.closure.subinterp(1)
        interp.values[0] = instance
        return YaploxFunction(self.declaration, interp, self.is_initializer)

    @jit.unroll_safe
    def call(self, arguments):
        declaration = jit.promote(self.declaration)
        subinterp = self.closure.subinterp(declaration.env_size)

        for i in range(len(declaration.params)):
            declared_token = declaration.params[i]
            argument = arguments[i]
            subinterp.values[i] = argument
        entrydriver.jit_merge_point(declaration=declaration, subinterp=subinterp, self=self)
        try:
            subinterp.execute_block(declaration.body)
        except YaploxReturnException as yaplox_return:
            if self.is_initializer:
                # When we're in init(), return this as an early return
                return self.closure.values[0]
            return yaplox_return.value

        if self.is_initializer:
            # When init() is called directly on a class
            return self.closure.values[0]

    def arity(self)  :
        jit.promote(self.declaration)
        return len(self.declaration.params)

    def __str__(self):
        return "<fn %s>" % (self.declaration.name.lexeme, )
