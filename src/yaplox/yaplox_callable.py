from yaplox import obj

class YaploxCallable(obj.W_Root):
    def call(self, arguments ):
        raise NotImplementedError

    def arity(self)  :
        raise NotImplementedError
