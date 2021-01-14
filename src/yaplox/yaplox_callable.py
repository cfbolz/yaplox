class YaploxCallable(object):
    def call(self, interpreter , arguments ):
        raise NotImplementedError

    def arity(self)  :
        raise NotImplementedError
