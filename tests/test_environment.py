import pytest

from yaplox.environment import Environment
from yaplox.token_type import TokenType
from yaplox.yaplox_runtime_error import YaploxRuntimeError


class TestEnvironment:
    def test_environment(self, create_token_factory):
        env = Environment()
        foo_token = create_token_factory(token_type=TokenType.VAR, lexeme="Foo")
        bar_token = create_token_factory(token_type=TokenType.VAR, lexeme="Bar")

        env.define("Foo", "Bar")

        assert env.get(foo_token) == "Bar"

        # This token isn't present
        with pytest.raises(YaploxRuntimeError):
            env.get(bar_token)

        # Test assign
        # Assign a new value to an existing key
        env.assign(foo_token, "New_value")

        assert env.get(foo_token) == "New_value"

        # Assigning to a new value is not possible
        with pytest.raises(YaploxRuntimeError):
            env.assign(bar_token, "Foo")

    @pytest.mark.parametrize("falsy_values", [0.0, 0, False, None])
    def test_falsy_values(self, create_token_factory, falsy_values):
        # Set a key with the value 0.0.
        # In python this is evaluated as false, but we want this value back!
        env = Environment()
        foo_token = create_token_factory(token_type=TokenType.VAR, lexeme="Foo")

        env.define("Foo", falsy_values)

        if isinstance(falsy_values, bool):
            assert env.get(foo_token) is falsy_values
        else:
            assert env.get(foo_token) == falsy_values

    def test_environment_enclosure(self, create_token_factory):
        global_env = Environment()
        local_env = Environment(enclosing=global_env)

        # Set a value to the global, that is available in local
        foo_token = create_token_factory(token_type=TokenType.VAR, lexeme="Foo")
        global_env.define("Foo", "42")

        # And retrieve it in the local env:
        assert local_env.get(foo_token) == "42"

        # Assign it a new value in the local env should also work:
        local_env.assign(foo_token, "New value")

        # And retrieve it in the local env:
        assert global_env.get(foo_token) == "New value"
        assert local_env.get(foo_token) == "New value"

        # Override the value in the local env:
        local_env.define("Foo", "Local variable")

        # This must override the local env, but keep global env the same.
        assert global_env.get(foo_token) == "New value"
        assert local_env.get(foo_token) == "Local variable"

    def test_environment_distance(self, create_token_factory):
        # Setup a few linked Environments
        global_env = Environment()
        local_1 = Environment(enclosing=global_env)
        local_2 = Environment(enclosing=local_1)
        local_3 = Environment(enclosing=local_2)

        # Set some variables:
        # Set a value to the global, that is available in local
        create_token_factory(token_type=TokenType.VAR, lexeme="global_token")
        global_env.define("global_token", "global_token")

        # Set a variable on the 1st level:
        create_token_factory(token_type=TokenType.VAR, lexeme="level_1")
        local_1.define("level_1", "level_1")

        # Get at a distance:
        assert local_3.get_at(2, "level_1") == "level_1"

        # It shouldn't be able to find this, level too shallow
        assert local_3.get_at(1, "level_1") is None

        # And try to find a global var
        assert local_3.get_at(3, "global_token") == "global_token"
