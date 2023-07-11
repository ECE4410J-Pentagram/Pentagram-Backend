import os
from . import dev
from . import prod


def get_config():
    env = os.environ.get("ENV", "dev")
    if env == "dev":
        return dev.Config()
    elif env == "prod":
        return prod.Config()
    else:
        raise ValueError(f"Invalid environment: {env}")


config = get_config()
