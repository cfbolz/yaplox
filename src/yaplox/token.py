from yaplox.token_type import TokenType


class Token:
    """
    Store parsed tokens
    """

    def __init__(self, token_type , lexeme , literal , line ):
        """
        Create a new Token. In the Lox documentation `token_type` is called `type`.
        It has been renamed since `type` is a reserved keyword
        """
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return "%s %s %s" % (self.token_type, self.lexeme, self.literal)
