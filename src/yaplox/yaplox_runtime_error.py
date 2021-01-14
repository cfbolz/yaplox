from yaplox.token import Token

class YaploxRuntimeError(Exception):
    def __init__(self, token, message):
        assert token is None or isinstance(token, Token)
        self.token = token
        self.message = message
