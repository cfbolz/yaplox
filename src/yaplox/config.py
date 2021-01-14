import logging

from classyconf import Configuration, EnvFile, Environment, EnvPrefix, Value, as_boolean


class AppConfig(Configuration):
    """Configuration for Yaplox"""

    class Meta:
        loaders = [
            Environment(keyfmt=EnvPrefix("YAPLOX_")),
            EnvFile(".env"),
        ]

    DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging mode.")



config = AppConfig()
