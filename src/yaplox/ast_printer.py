from yaplox.expr import (
    Assign,
    Binary,
    Call,
    Expr,
    ExprVisitor,
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


class AstPrinter(ExprVisitor):
    def visit_assign_expr(self, expr ):
        raise NotImplementedError

    def visit_binary_expr(self, expr ):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr ):
        raise NotImplementedError

    def visit_get_expr(self, expr ):
        pass

    def visit_grouping_expr(self, expr ):
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr ):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr ):
        raise NotImplementedError

    def visit_set_expr(self, expr ):
        pass

    def visit_super_expr(self, expr ):
        pass

    def visit_this_expr(self, expr ):
        pass

    def visit_unary_expr(self, expr ):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr ):
        raise NotImplementedError

    def print(self, expr )  :
        return expr.accept(self)

    def _parenthesize(self, name , *args ):
        expressions = ["(", name]

        for expr in args:
            expressions.append(" ")
            expressions.append(expr.accept(self))

        expressions.append(")")

        return "".join(expressions)
