from yaplox.expr import Base, ExprVisitor, Expr, Variable
from yaplox.token import Token


class EverythingVisitor(ExprVisitor):
    """This class is used as an Vistor for the Stmt class"""

    def visit_block_stmt(self, stmt ):
        raise NotImplementedError

    def visit_class_stmt(self, stmt ):
        raise NotImplementedError

    def visit_expression_stmt(self, stmt ):
        raise NotImplementedError

    def visit_function_stmt(self, stmt ):
        raise NotImplementedError

    def visit_if_stmt(self, stmt ):
        raise NotImplementedError

    def visit_print_stmt(self, stmt ):
        raise NotImplementedError

    def visit_return_stmt(self, stmt ):
        raise NotImplementedError

    def visit_var_stmt(self, stmt ):
        raise NotImplementedError

    def visit_while_stmt(self, stmt ):
        raise NotImplementedError


class Stmt(Base):
    def accept(self, visitor ):
        raise NotImplementedError

class EnvHaver(Stmt):
    _immutable_fields_ = ['env_size']

    env_size = -1 # assigned by the resolver

class Block(EnvHaver):
    _immutable_fields_ = ['statements']

    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_block_stmt(self)


class Class(EnvHaver):
    _immutable_fields_ = ['name', 'superclass', 'methods']

    def __init__(
        self, name , superclass , methods 
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_class_stmt(self)


class Expression(Stmt):
    _immutable_fields_ = ['expression']
    def __init__(self, expression ):
        self.expression = expression

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_expression_stmt(self)


class Function(EnvHaver):
    _immutable_fields_ = ['environment_distance', 'environment_index', 'name', 'params[*]', 'body']

    environment_distance = -1 # where is the function defined
    environment_index = -1

    def __init__(self, name , params , body ):
        self.name = name
        self.params = params[:]
        self.body = body

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_function_stmt(self)


class If(Stmt):
    _immutable_fields_ = ['condition', 'then_branch', 'else_branch']
    def __init__(self, condition , then_branch , else_branch ):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_if_stmt(self)


class Print(Stmt):
    def __init__(self, expression ):
        self.expression = expression

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_print_stmt(self)


class Return(Stmt):
    _immutable_fields_ = ['keyword', 'value']
    def __init__(self, keyword , value ):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_return_stmt(self)


class Var(Stmt):
    _immutable_fields_ = ['name', 'initializer']
    def __init__(self, name , initializer ):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_var_stmt(self)


class While(Stmt):
    _immutable_fields_ = ['condition', 'body']
    def __init__(self, condition , body ):
        self.condition = condition
        self.body = body

    def accept(self, visitor ):
        """ Create a accept method that calls the visitor. """
        return visitor.visit_while_stmt(self)

class Program(object):
    def __init__(self, statements):
        self.statements = statements
        
