from yaplox.stmt import Function
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_instance import YaploxInstance
from yaplox.yaplox_return_exception import YaploxReturnException


class YaploxFunction(YaploxCallable):
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
        interp = self.closure.subinterp(1)
        interp.values[0] = instance
        return YaploxFunction(self.declaration, interp, self.is_initializer)

    def call(self, arguments):
        subinterp = self.closure.subinterp(self.declaration.env_size)

        for i in range(len(self.declaration.params)):
            declared_token = self.declaration.params[i]
            argument = arguments[i]
            subinterp.values[i] = argument
        try:
            subinterp.execute_block(self.declaration.body)
        except YaploxReturnException as yaplox_return:
            if self.is_initializer:
                # When we're in init(), return this as an early return
                return self.closure.values[0]
            return yaplox_return.value

        if self.is_initializer:
            # When init() is called directly on a class
            return self.closure.values[0]

    def arity(self)  :
        return len(self.declaration.params)

    def __str__(self):
        return "<fn %s>" % (self.declaration.name.lexeme, )
