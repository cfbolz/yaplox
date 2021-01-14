class YaploxRuntimeError(Exception):
    def __init__(self, token, message):
        Exception.__init__(self, message)
        self.token = token
        self.message = message
