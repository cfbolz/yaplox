
from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError

class Globals(object):
    def __init__(self):
        self.globals = {}


    def get(self, name):
        return self.globals.get(name)

    def assign(self, name, w_val):
        self.globals[name] = w_val
    define = assign


class Environment:
    def __init__(self, size, enclosing):
        self.values   = [None] * size
        self.enclosing = enclosing

    def define(self, position , value ):
        self.values[position] = value

    def _ancestor(self, distance )  :
        environment = self

        for _ in range(distance):
            environment = environment.enclosing  # type: ignore

        return environment

    def get_at(self, distance, position, name)  :
        """
        Return a variable at a distance
        """
        return self._ancestor(distance=distance).values[position]

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

    def assign_at(self, distance, position, value):
        self._ancestor(distance).values[position] = value
