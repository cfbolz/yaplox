
from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError


class Environment:
    def __init__(self, enclosing  = None):
        self.values   = dict()
        self.enclosing = enclosing

    def define(self, name , value ):
        self.values[name] = value

    def _ancestor(self, distance )  :
        environment = self

        for _ in range(distance):
            environment = environment.enclosing  # type: ignore

        return environment

    def get_at(self, distance , name )  :
        """
        Return a variable at a distance
        """
        return self._ancestor(distance=distance).values.get(name)

    def get(self, name )  :
        try:
            return self.values[name.lexeme]
        except KeyError:
            # We ignore this key error, if an nested Environment is available, test this
            # first.
            pass

        if self.enclosing:
            return self.enclosing.get(name)

        raise YaploxRuntimeError(name, "Undefined variable '%s'." % (name.lexeme, ))

    def assign(self, name , value ):
        """Assign a new value to an existing variable. Eg:
        var a = 3;
        a = 4  # This calls assign.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise YaploxRuntimeError(name, "Undefined variable '%s'." % (name.lexeme, ))

    def assign_at(self, distance , name , value ):
        self._ancestor(distance).values[name.lexeme] = value
