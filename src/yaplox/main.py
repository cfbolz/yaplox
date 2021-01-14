import sys


from yaplox.interpreter import Interpreter
from yaplox.parser import Parser
from yaplox.resolver import Resolver
from yaplox.scanner import Scanner
from yaplox.token import Token
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError



class Yaplox:
    def __init__(self):
        self.had_error  = False
        self.had_runtime_error  = False
        self.interpreter  = Interpreter()

    def run(self, source ):

        scanner = Scanner(source, on_error=self.error)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, on_token_error=self.token_error)
        statements = parser.parse()

        if self.had_error:
            print("Error after parsing")
            return

        resolver = Resolver(interpreter=self.interpreter, on_error=self.token_error)
        resolver.resolve(statements)
        # Stop if there was a resolution error.
        if self.had_error:
            print("Error after resolving")
            return

        self.interpreter.interpret(statements, on_error=self.runtime_error)

    def error(self, line , message ):
        self.report(line, "", message)

    def runtime_error(self, error ):
        message = "%s in line [line%s]" % (str(error.message), error.token.line)
        print(message)
        self.had_runtime_error = True

    def token_error(self, token , message ):
        if token.token_type == TokenType.EOF:
            self.report(token.line, " At end ", message)
        else:
            self.report(token.line, " at '%s'" % (token.lexeme, ), message)

    def report(self, line , where , message ):
        message = "[line %s] Error %s : %s" % (line, where, message)
        print(message)
        self.had_error = True

    @staticmethod
    def _load_file(file )  :  # pragma: no cover
        f = open(file)
        try:
            content = f.read()
        finally:
            f.close()
        return content

    def run_file(self, file ):  # pragma: no cover
        """
        Run yaplox with `file` as filename for the source input
        """
        lines = self._load_file(file)
        self.run(lines)

        # Indicate an error in the exit code
        if self.had_error:
            return 65

        if self.had_runtime_error:
            return 70
        return 0

    def run_prompt(self):  # pragma: no cover
        """
        Run a REPL prompt. This prompt can be quit by pressing CTRL-C or CTRL-D
        """
        print("Welcome to Yaplox")
        print("Press CTRL-C or CTRL-D to exit")

        while True:
            try:
                str_input = input("> ")
                if str_input and str_input[0] == chr(4):
                    # Catch ctrl-D and raise as error
                    raise EOFError

                self.run(str_input)
                self.had_error = False

            except (KeyboardInterrupt, EOFError):
                # Catch CTRL-C or CTRL-D (EOF)
                self.quit_gracefully()

    def quit_gracefully(self):  # pragma: no cover
        print("So Long, and Thanks for All the Fish")
        sys.exit(0)

    @staticmethod
    def main():  # pragma: no cover
        """
        Run Yaplox from the console. Accepts one argument as a file that will be
        executed, or no arguments to run in REPL mode.
        """
        if len(sys.argv) > 2:
            print("Usage: %s [script]" % (sys.argv[0], ))
            sys.exit(64)
        elif len(sys.argv) == 2:
            Yaplox().run_file(sys.argv[1])
        else:
            Yaplox().run_prompt()
