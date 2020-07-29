import pytest

from yaplox.scanner import Scanner
from yaplox.token_type import TokenType


class TestScanner:
    def test_scanner(self, mocker):
        on_error_mock = mocker.MagicMock()

        source = "+-*"
        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()
        assert tokens[0].token_type == TokenType.PLUS
        assert tokens[1].token_type == TokenType.MINUS
        assert tokens[2].token_type == TokenType.STAR

        # the EOF is automatically added
        assert tokens[3].token_type == TokenType.EOF

        # There musn't be an error
        assert not on_error_mock.called

    @pytest.mark.parametrize(
        ("source", "expected_output_list"),
        [
            ("+-*", [TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.EOF]),
            ("!=", [TokenType.BANG_EQUAL, TokenType.EOF]),
            ("!", [TokenType.BANG, TokenType.EOF]),
            ("==", [TokenType.EQUAL_EQUAL, TokenType.EOF]),
            ("=", [TokenType.EQUAL, TokenType.EOF]),
            ("===", [TokenType.EQUAL_EQUAL, TokenType.EQUAL, TokenType.EOF]),
            (">", [TokenType.GREATER, TokenType.EOF]),
            (">=", [TokenType.GREATER_EQUAL, TokenType.EOF]),
            ("<", [TokenType.LESS, TokenType.EOF]),
            ("<=", [TokenType.LESS_EQUAL, TokenType.EOF]),
        ],
    )
    def test_scanner_operator(self, source, expected_output_list, mocker):
        on_error_mock = mocker.MagicMock()

        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()

        # Retrieve the token_types from the created tokens
        token_types = [token.token_type for token in tokens]

        assert token_types == expected_output_list
        assert not on_error_mock.called

    def test_scanner_bad_char(self, mocker):
        source = "@"
        on_error_mock = mocker.MagicMock()
        scanner = Scanner(source, on_error=on_error_mock)
        tokens = scanner.scan_tokens()

        # Invalid character is not added, but the EOF marker is added
        assert tokens[0].token_type == TokenType.EOF
        assert tokens[0].line == 1

        # Assert that our error code has been called
        assert on_error_mock.called
        on_error_mock.assert_called_once_with(1, "Unexpected character: @")

    def test_scanner_bad_char_without_callback(self):
        source = "@"
        scanner = Scanner(source)
        with pytest.raises(KeyError):
            scanner.scan_tokens()