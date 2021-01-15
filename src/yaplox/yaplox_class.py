from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_function import YaploxFunction
from yaplox.yaplox_instance import YaploxInstance


class YaploxClass(YaploxCallable):
    def call(self, arguments):
        instance = YaploxInstance(klass=self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance=instance).call(
                arguments
            )
        return instance

    def arity(self)  :
        initializer = self.find_method("init")
        if initializer is not None:
            return initializer.arity()
        else:
            return 0

    def __init__(
        self,
        name ,
        superclass ,
        methods  ,
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __repr__(self):
        return self.name

    def find_method(self, name )  :
        try:
            return self.methods[name]
        except KeyError:
            pass

        if self.superclass:
            return self.superclass.find_method(name)

        return None
