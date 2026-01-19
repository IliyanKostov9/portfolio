import os


def check_if_env_vars_are_set(env_vars: list[str]) -> None:
    """
    Check if environment variable is set and raise an error if that's not the case

    """
    for env_var in env_vars:
        if not os.environ.get(env_var):
            raise ValueError(f"Environment variable {env_var} is NOT SET!")
