counter = 0
def auto():
    global counter
    res = counter
    counter += 1
    return res

class TokenType(object):
    """
    Tokens that are used in the Language. The mapping from number to character
    will be done in the scanner.
    """

    #
    # Single - character tokens.
    #
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    #
    # One or two character tokens.
    #
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    #
    # Literals.
    #
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    #
    # Keywords.
    #
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()
