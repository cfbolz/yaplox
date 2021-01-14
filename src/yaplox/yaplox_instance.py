from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from yaplox.token import Token
from yaplox.yaplox_runtime_error import YaploxRuntimeError

if TYPE_CHECKING:
    from yaplox.yaplox_class import YaploxClass


class YaploxInstance:
    def __init__(self, klass ):
        self.klass = klass
        self.fields   = {}

    def __repr__(self)  :
        return f"{self.klass.name} instance"

    def get(self, name )  :
        try:
            return self.fields[name.lexeme]
        except KeyError:
            pass

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise YaploxRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name , value ):
        self.fields[name.lexeme] = value
