from yaplox.token import Token


class ExprVisitor(object):
    """This class is used as an Vistor for the Expr class"""

    def visit_assign_expr(self, expr ):
        raise NotImplementedError

    def visit_binary_expr(self, expr ):
        raise NotImplementedError

    def visit_call_expr(self, expr ):
        raise NotImplementedError

    def visit_get_expr(self, expr ):
        raise NotImplementedError

    def visit_grouping_expr(self, expr ):
        raise NotImplementedError

    def visit_literal_expr(self, expr ):
        raise NotImplementedError

    def visit_logical_expr(self, expr ):
        raise NotImplementedError

    def visit_set_expr(self, expr ):
        raise NotImplementedError

    def visit_super_expr(self, expr ):
        raise NotImplementedError

    def visit_this_expr(self, expr ):
        raise NotImplementedError

    def visit_unary_expr(self, expr ):
        raise NotImplementedError

    def visit_variable_expr(self, expr ):
        raise NotImplementedError

class Base(object):
    def accept(self, visitor ):
        raise NotImplementedError


class Expr(Base):
    pass

class EnvEntry(Expr):
    _immutable_fields_ = ['environment_index', 'environment_distance']

    environment_distance = -1 # -1 means global, positive number is distance of environments
    environment_index = -1 # will be assigned by resolved


class Assign(EnvEntry):
    _immutable_fields_ = ['name', 'value']
    def __init__(self, name , value ):
        self.name = name
        self.value = value

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    _immutable_fields_ = ['left', 'operator', 'right']
    def __init__(self, left , operator , right ):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_binary_expr(self)


class Call(Expr):
    _immutable_fields_ = ['callee', 'paren', 'arguments[*]']
    def __init__(self, callee , paren , arguments ):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments[:]

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_call_expr(self)


class Get(Expr):
    _immutable_fields_ = ['obj', 'name']
    def __init__(self, obj , name ):
        self.obj = obj
        self.name = name

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_get_expr(self)


class Grouping(Expr):
    _immutable_fields_ = ['expression']
    def __init__(self, expression ):
        self.expression = expression

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    _immutable_fields_ = ['value']
    def __init__(self, value ):
        self.value = value

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    _immutable_fields_ = ['left', 'operator', 'right']
    def __init__(self, left , operator , right ):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_logical_expr(self)


class Set(Expr):
    _immutable_fields_ = ['obj', 'name', 'value']
    def __init__(self, obj , name , value ):
        self.obj = obj
        self.name = name
        self.value = value

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_set_expr(self)


class Super(EnvEntry):
    def __init__(self, keyword , method ):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_super_expr(self)


class This(EnvEntry):
    _immutable_fields_ = ['keyword']
    def __init__(self, keyword ):
        self.keyword = keyword

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_this_expr(self)


class Unary(Expr):
    _immutable_fields_ = ['operator', 'right']
    def __init__(self, operator , right ):
        self.operator = operator
        self.right = right

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_unary_expr(self)


class Variable(EnvEntry):
    _immutable_fields_ = ['name']
    def __init__(self, name ):
        self.name = name

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_variable_expr(self)
