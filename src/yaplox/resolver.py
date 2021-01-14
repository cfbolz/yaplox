from collections import deque


from yaplox.class_type import ClassType
from yaplox.expr import (
    Assign,
    Binary,
    Call,
    Expr,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    Super,
    This,
    Unary,
    Variable,
)
from yaplox.function_type import FunctionType
from yaplox.interpreter import Interpreter
from yaplox.stmt import (
    Block,
    Class,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    EverythingVisitor,
    Var,
    While,
)
from yaplox.token import Token



class Resolver(EverythingVisitor):
    def __init__(self, interpreter , on_error=None):
        self.interpreter = interpreter
        self.scopes  = []
        self.on_error = on_error
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, statements ):
        self._resolve_statements(statements)

    def _resolve_statements(self, statements ):
        for statement in statements:
            self._resolve_statement(statement)

    def _resolve_statement(self, statement ):
        statement.accept(self)

    def _resolve_expression(self, expression ):
        expression.accept(self)

    def _resolve_local(self, expr , name ):
        #for idx, scope in enumerate(reversed(self.scopes)):
        for i in range(len(self.scopes) - 1, -1, -1):
            idx = len(self.scopes) - 1 - i
            scope = self.scopes[i]
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                return
        # Not found. Assume it is global.

    def _resolve_function(self, function , type ):
        enclosing_function = self.current_function
        self.current_function = type

        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)

        self._resolve_statements(function.body)
        self._end_scope()
        self.current_function = enclosing_function

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name ):
        """
        Declare that a variable exists
        Example is `var a;`
        """
        if len(self.scopes) == 0:
            return

        # Look at the last scope
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.on_error(name, "Already variable with this name in this scope.")

        scope[name.lexeme] = False

    def _define(self, name ):
        """
        Declare that a variable is ready to use
        Example: `a = 42;`
        """

        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def visit_assign_expr(self, expr ):
        self._resolve_expression(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr ):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)

    def visit_call_expr(self, expr ):
        self._resolve_expression(expr.callee)

        for argument in expr.arguments:
            self._resolve_expression(argument)

    def visit_get_expr(self, expr ):
        self._resolve_expression(expr.obj)

    def visit_grouping_expr(self, expr ):
        self._resolve_expression(expr.expression)

    def visit_literal_expr(self, expr ):
        """
        Since a literal expression doesn't mention any variables and doesn't
        contain any subexpressions, there is no work to do.
        """
        return

    def visit_logical_expr(self, expr ):
        self._resolve_expression(expr.left)
        self._resolve_expression(expr.right)

    def visit_this_expr(self, expr ):
        if self.current_class == ClassType.NONE:
            self.on_error(expr.keyword, "Can't use 'this' outside of a class.")

        self._resolve_local(expr, expr.keyword)

    def visit_set_expr(self, expr ):
        self._resolve_expression(expr.value)
        self._resolve_expression(expr.obj)

    def visit_super_expr(self, expr ):
        if self.current_class == ClassType.NONE:
            self.on_error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.current_class != ClassType.SUBCLASS:
            self.on_error(
                expr.keyword, "Can't use 'super' in a class with no superclass."
            )

        self._resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr ):
        self._resolve_expression(expr.right)

    def visit_variable_expr(self, expr ):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme, True) == False:
            self.on_error(
                expr.name, "Cannot read local variable in its own initializer."
            )
        self._resolve_local(expr, expr.name)

    def visit_block_stmt(self, stmt ):
        self._begin_scope()
        self._resolve_statements(stmt.statements)
        self._end_scope()

    def visit_class_stmt(self, stmt ):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self._declare(stmt.name)
        self._define(stmt.name)

        if stmt.superclass and stmt.name.lexeme == stmt.superclass.name.lexeme:
            self.on_error(stmt.superclass.name, "A class can't inherit from itself.")

        if stmt.superclass is not None:
            self.current_class = ClassType.SUBCLASS
            self._resolve_expression(stmt.superclass)

        if stmt.superclass is not None:
            self._begin_scope()
            self.scopes[-1]["super"] = True

        self._begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER

            self._resolve_function(method, declaration)

        self._end_scope()

        if stmt.superclass is not None:
            self._end_scope()

        self.current_class = enclosing_class

    def visit_expression_stmt(self, stmt ):
        self._resolve_expression(stmt.expression)

    def visit_function_stmt(self, stmt ):
        self._declare(stmt.name)
        self._define(stmt.name)

        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt ):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.then_branch)
        if stmt.else_branch:
            self._resolve_statement(stmt.else_branch)

    def visit_print_stmt(self, stmt ):
        self._resolve_expression(stmt.expression)

    def visit_return_stmt(self, stmt ):
        if self.current_function == FunctionType.NONE:
            self.on_error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value:
            if self.current_function == FunctionType.INITIALIZER:
                self.on_error(stmt.keyword, "Can't return a value from an initializer.")
            self._resolve_expression(stmt.value)

    def visit_var_stmt(self, stmt ):
        self._declare(stmt.name)

        if stmt.initializer is not None:
            self._resolve_expression(stmt.initializer)

        self._define(stmt.name)

    def visit_while_stmt(self, stmt ):
        self._resolve_expression(stmt.condition)
        self._resolve_statement(stmt.body)
