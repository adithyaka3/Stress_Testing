import functools
import os
from typing import Callable

def change_directory_to_root(func: Callable) -> Callable:
    """
    Decorator to temporarily change the working directory to the project root
    (where stress_testing.py is located) for the duration of the decorated function call.
    """
    @functools.wraps(func)
    def wrapper_change_directory_to_root(*args, **kwargs):
        current_directory = os.getcwd()
        # Project root is the parent of the parent of this file (src/utils/ -> src/ -> project root)
        root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        try:
            os.chdir(root_directory)
            return func(*args, **kwargs)
        finally:
            os.chdir(current_directory)
    return wrapper_change_directory_to_root


@change_directory_to_root
def delete_file(file_path: str) -> None:
    """
    Delete a file at the given relative path from the project root.
    Does nothing if the file does not exist.
    """
    full_path = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(full_path):
        os.remove(full_path)


@change_directory_to_root
def clean_up() -> None:
    """
    Remove common build/test artifacts from cpp directory.
    """
    for base in ("generator", "correct", "test"):
        delete_file(os.path.join("cpp", base))
        delete_file(os.path.join("cpp", base + ".exe"))
