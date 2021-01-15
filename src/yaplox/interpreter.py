from rpython.rlib import jit

from yaplox.clock import Clock
from yaplox.environment import Globals
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
from yaplox.token_type import TokenType
from yaplox.yaplox_callable import YaploxCallable
from yaplox.yaplox_class import YaploxClass
from yaplox.yaplox_function import YaploxFunction
from yaplox.yaplox_instance import YaploxInstance
from yaplox.yaplox_return_exception import YaploxReturnException
from yaplox.yaplox_runtime_error import YaploxRuntimeError
from yaplox import obj



class Interpreter(EverythingVisitor):
    def __init__(self, size=0, enclosing=None, globals=None):
        if globals is None:
            if enclosing is None:
                self.globals = Globals()
                self.globals.define("clock", Clock())
            else:
                self.globals = enclosing.globals
        else:
            self.globals = globals
        self.values   = [None] * size
        self.enclosing = enclosing

    def subinterp(self, size):
        return Interpreter(size, self)

    def _ancestor(self, distance )  :
        environment = self

        for _ in range(distance):
            environment = environment.enclosing  # type: ignore

        return environment

    def define(self, distance, position, name, w_val):
        if distance == -1:
            self.globals.define(name, w_val)
            return
        assert distance == 0
        self.values[position] = w_val

    def assign(self, distance, position, name, w_val):
        if distance == -1:
            self.globals.assign(name, w_val)
            return
        self._ancestor(distance).values[position] = w_val

    def interpret(self, program, on_error=None)  :
        try:
            res = None
            for statement in program.statements:
                res = self._execute(statement)
            # The return in the interpreter is not default Lox. It's added for now
            # to make testing and debugging easier.
            return res
        except YaploxRuntimeError as excp:
            on_error(excp)

    def _execute(self, stmt ):
        return stmt.accept(self)

    @staticmethod
    def _stringify(o)  :
        return o.str()

    @staticmethod
    def _binary_plus(expr, left, right):
        if isinstance(left, obj.W_Number) and isinstance(right, obj.W_Number):
            return obj.W_Number(left.num + right.num)

        if isinstance(left, obj.W_String) and isinstance(right, obj.W_String):
            return obj.W_String(left.val + right.val)

        raise YaploxRuntimeError(
            expr.operator, "Operands must be two numbers or two strings"
        )

    @staticmethod
    def _is_equal(a, b)  :
        if a is None and b is None:
            return True

        if a is None:
            return False

        return a == b

    def visit_binary_expr(self, expr ):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        token_type = expr.operator.token_type

        if token_type == TokenType.GREATER:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval > rightval)
        elif token_type == TokenType.GREATER_EQUAL:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval >= rightval)
        elif token_type == TokenType.LESS:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval < rightval)
        elif token_type == TokenType.LESS_EQUAL:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval <= rightval)
        elif token_type == TokenType.EQUAL_EQUAL:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval == rightval)
        elif token_type == TokenType.BANG_EQUAL:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.newbool(leftval <= rightval)
        elif token_type == TokenType.MINUS:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.W_Number(leftval - rightval)
        elif token_type == TokenType.SLASH:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.W_Number(leftval / rightval)
        elif token_type == TokenType.STAR:
            leftval, rightval = self._check_number_operands(expr.operator, left, right)
            return obj.W_Number(leftval * rightval)
        elif token_type == TokenType.PLUS:
            return self._binary_plus(expr, left, right)
        else:
            raise YaploxRuntimeError(
                expr.operator, "Unknown operator %s" % (expr.operator.lexeme, )
            )

    def visit_call_expr(self, expr ):
        function = self._evaluate(expr.callee)

        arguments = [self._evaluate(argument) for argument in expr.arguments]

        if not isinstance(function, YaploxCallable):
            raise YaploxRuntimeError(expr.paren, "Can only call functions and classes.")

        # function = YaploxCallable(callee)
        if len(arguments) != function.arity():
            raise YaploxRuntimeError(
                expr.paren,
                "Expected %s arguments but got %s." % (function.arity(), len(arguments)),
            )
        return function.call(arguments)

    def visit_get_expr(self, expr ):
        obj = self._evaluate(expr.obj)
        if isinstance(obj, YaploxInstance):
            return obj.get(expr.name)

        raise YaploxRuntimeError(expr.name, "Only instances have properties.")

    def visit_grouping_expr(self, expr ):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr ):
        return expr.value

    def visit_logical_expr(self, expr ):
        left = self._evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def visit_set_expr(self, expr ):
        obj = self._evaluate(expr.obj)

        if not isinstance(obj, YaploxInstance):
            raise YaploxRuntimeError(expr.name, "Only instances have fields.")

        value = self._evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visit_super_expr(self, expr ):
        assert 0, "broken"
        distance = expr.environment_distance
        superclass  = self.environment.get_at(
            distance=distance, name="super"
        )
        obj = self.environment.get_at(distance=distance - 1, name="this")
        method = superclass.find_method(expr.method.lexeme)

        # Check that we have a super method
        if method is None:
            raise YaploxRuntimeError(
                expr.method, "Undefined property '%s'." % (expr.method.lexeme, )
            )
        return method.bind(obj)

    def visit_this_expr(self, expr ):
        return self._look_up_variable(expr.keyword, expr)

    def visit_unary_expr(self, expr ):
        right = self._evaluate(expr.right)

        token_type = expr.operator.token_type
        if token_type == TokenType.MINUS:
            rightval = self._check_number_operand(expr.operator, right)
            return obj.W_Number(-rightval)
        elif token_type == TokenType.BANG:
            return obj.newbool(not Interpreter._is_truthy(right))
        else:
            raise YaploxRuntimeError(expr.operator, "unknown unary operator")


    @staticmethod
    def _check_number_operand(operator , operand ):
        if isinstance(operand, obj.W_Number):
            return operand.num
        raise YaploxRuntimeError(operator, "%s must be a number." % (operand, ))

    @staticmethod
    def _check_number_operands(operator , left , right ):
        if isinstance(left, obj.W_Number) and isinstance(right, obj.W_Number):
            return left.num, right.num
        raise YaploxRuntimeError(operator, "Operands must be numbers.")

    @staticmethod
    def _is_truthy(o):
        if o is obj.w_nil:
            return False

        if o is obj.w_false:
            return False

        return True

    def _evaluate(self, expr ):
        return expr.accept(self)

    def visit_variable_expr(self, expr )  :
        return self._look_up_variable(expr.name, expr)

    def _look_up_variable(self, name , expr )  :
        distance = expr.environment_distance
        position = expr.environment_index
        if distance >= 0:
            return self._ancestor(distance=distance).values[position]
        else:
            return self.globals.get(name.lexeme)

    def visit_assign_expr(self, expr )  :
        value = self._evaluate(expr.value)
        distance = expr.environment_distance
        self.assign(distance, expr.environment_index, expr.name.lexeme, value)
        return value

    # statement stuff
    def visit_class_stmt(self, stmt ):
        superclass = None
        if stmt.superclass is not None:
            superclass = self._evaluate(stmt.superclass)
            if not isinstance(superclass, YaploxClass):
                raise YaploxRuntimeError(
                    stmt.superclass.name, "Superclass must be a class."
                )

        self.define(stmt.environment_distance, stmt.environment_index, stmt.name.lexeme, obj.w_nil)

        if stmt.superclass is not None:
            self = self.subinterp(1)
            self.values[0] = superclass

        methods   = {}

        for method in stmt.methods:
            function = YaploxFunction(
                method, self, method.name.lexeme == "init"
            )
            methods[method.name.lexeme] = function

        klass = YaploxClass(
            name=stmt.name.lexeme, superclass=superclass, methods=methods
        )

        if stmt.superclass is not None:
            self = self.enclosing
        self.assign(stmt.environment_distance, stmt.environment_index, stmt.name.lexeme, klass)

    def visit_expression_stmt(self, stmt):
        return self._evaluate(stmt.expression)

    def visit_function_stmt(self, stmt):
        function = YaploxFunction(stmt, self, False)
        self.define(stmt.environment_distance, stmt.environment_index, stmt.name.lexeme, function)

    def visit_if_stmt(self, stmt )  :
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def visit_while_stmt(self, stmt )  :
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def visit_print_stmt(self, stmt )  :
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_return_stmt(self, stmt )  :
        value = None
        if stmt.value:
            value = self._evaluate(stmt.value)
        raise YaploxReturnException(value=value)

    def visit_var_stmt(self, stmt )  :
        value = obj.w_nil
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)

        self.define(stmt.environment_distance, stmt.environment_index, stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt )  :
        self.subinterp(stmt.env_size).execute_block(stmt.statements)

    def execute_block(self, statements):
        for statement in statements:
            self._execute(statement)
