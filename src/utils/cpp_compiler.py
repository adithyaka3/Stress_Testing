import os
import subprocess
import platform
from contextlib import nullcontext
from typing import Optional
from pathlib import Path
from .file_handler import change_directory_to_root


def get_executable_extension() -> str:
    """Return the executable extension for the current OS."""
    return ".exe" if platform.system().lower() == "windows" else ""


def get_default_compiler() -> str:
    """Return the default C++ compiler for the current OS, with env override and fallback."""
    compiler = os.environ.get("CXX")
    if compiler:
        return compiler
    system = platform.system().lower()
    if system == "darwin":
        # Prefer c++ (AppleClang), fallback to clang++
        from shutil import which
        if which("c++"):
            return "c++"
        if which("clang++"):
            return "clang++"
        return "g++"  # fallback, but not recommended on macOS
    return "g++"


@change_directory_to_root
def compile_file(file_name: str, output_dir: str = "cpp") -> None:
    """
    Compile a C++ file in the given directory.
    Args:
        file_name: Name of the C++ file (without .cpp extension)
        output_dir: Directory containing the C++ file (default: 'cpp')
    Raises:
        ValueError: If compilation fails.
    """
    file_path = Path(output_dir) / file_name
    output_file = str(file_path) + get_executable_extension()
    # Check if file exists before compiling
    if not (file_path.with_suffix('.cpp')).is_file():
        raise ValueError(f"Source file '{file_path.with_suffix('.cpp')}' not found.")
    command = [get_default_compiler(), "-std=c++17", f"{file_path}.cpp", "-o", output_file]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Compilation Error in {file_name}.cpp ⚠️\n{e.stderr}")


def _get_file_path(base_dir: str, file_name: Optional[str]) -> Optional[str]:
    if file_name:
        return str(Path(base_dir) / file_name)
    return None


@change_directory_to_root
def run_file(
    file_name: str,
    input_file_name: Optional[str] = None,
    output_file_name: Optional[str] = None,
    time_limit: float = 2.0,
):
    """
    Run a compiled C++ executable with optional input/output redirection and time limit.
    Args:
        file_name: Name of the executable (without extension)
        input_file_name: Input file name (from 'data/')
        output_file_name: Output file name (to 'data/')
        time_limit: Time limit in seconds
    Raises:
        FileNotFoundError: If executable or input file is missing
        RuntimeError: If the program returns a non-zero exit code
        TimeoutError: If the program exceeds the time limit
    Returns:
        subprocess.CompletedProcess: The result of the run
    """
    file_path = str(Path("cpp") / (file_name + get_executable_extension()))
    input_path = _get_file_path("data", input_file_name)
    output_path = _get_file_path("data", output_file_name)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Executable '{file_path}' not found.")
    if input_path and not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' not found.")

    with open(input_path, "r") if input_path else nullcontext() as infile, \
         open(output_path, "w") if output_path else nullcontext() as outfile:
        command = [file_path]
        try:
            result = subprocess.run(
                command,
                check=True,
                timeout=time_limit,
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Runtime Error: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Time Limit Exceeded for {file_name}.cpp ⏳")
    return result


def normalize_output(output_file: str) -> list[str]:
    """
    Read and normalize output file into a list of tokens.
    Args:
        output_file: Output file name (from 'data/')
    Returns:
        List of tokens (strings)
    """
    output_path = str(Path.cwd() / "data" / output_file)
    if not os.path.isfile(output_path):
        return []
    with open(output_path, "r") as file:
        return [token for line in file for token in line.strip().split()]


@change_directory_to_root
def check_diff(output1: str, output2: str) -> bool:
    """
    Check if two output files are identical after normalization.
    Args:
        output1: First output file name (from 'data/')
        output2: Second output file name (from 'data/')
    Returns:
        True if outputs are identical, False otherwise
    """
    return normalize_output(output1) == normalize_output(output2)


@change_directory_to_root
def validate_errors(
    file_name: str,
    input_file_name: str,
    output_file_name: str,
    test: int,
    time_limit: float = 2.0,
):
    """
    Run a file and handle common errors, raising ValueError with a clear message.
    Args:
        file_name: Name of the executable (without extension)
        input_file_name: Input file name (from 'data/')
        output_file_name: Output file name (to 'data/')
        test: Test case number
        time_limit: Time limit in seconds
    Raises:
        ValueError: If file not found, runtime error, or time limit exceeded
    """
    try:
        return run_file(file_name, input_file_name, output_file_name, time_limit)
    except FileNotFoundError as e:
        raise ValueError(f"File not found: {e}")
    except RuntimeError as e:
        raise ValueError(f"Runtime Error in {file_name}.cpp on test case {test} ⚠️\n{e}")
    except TimeoutError:
        raise ValueError(
            f"Time Limit Exceeded in {file_name}.cpp on test case {test} ⏳"
        )


@change_directory_to_root
def print_output(output_file: str) -> None:
    """
    Print the contents of an output file.
    Args:
        output_file: Output file name (from 'data/')
    Raises:
        FileNotFoundError: If the file does not exist
    """
    output_path = str(Path("data") / output_file)
    if not os.path.isfile(output_path):
        raise FileNotFoundError(f"File '{output_path}' not found.")
    with open(output_path, "r") as file:
        print(file.read())
