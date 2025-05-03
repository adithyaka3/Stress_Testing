import os
import sys
import argparse
import platform

# Always change to project root before anything else
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))
from src.utils.terminal_colors import Colors
from src.utils import cpp_compiler
from src.utils import file_handler

def enable_windows_colors():
    if platform.system().lower() == "windows":
        os.system("")

def print_test_result(test_num, status, status_color, input_data, expected_output, your_output, file_name):
    # Map status to more descriptive colors and emojis
    status_styles = {
        "TIME LIMIT EXCEEDED": (Colors.fg.yellow, "⏳"),
        "WRONG ANSWER": (Colors.fg.red, "❌"),
        "RUNTIME ERROR": (Colors.fg.magenta, "💥"),
        "ACCEPTED": (Colors.fg.green, "✅"),
        "ERROR": (Colors.fg.red, "⚠️"),
    }
    color, emoji = status_styles.get(status, (status_color, "❔"))
    border = f"{Colors.fg.blue}{'═'*60}{Colors.reset}"
    section = f"{Colors.fg.cyan}{'─'*60}{Colors.reset}"
    sub_border = f"{Colors.fg.lightblue}{'-'*60}{Colors.reset}"
    print(border)
    print(f"{Colors.fg.purple}🧪 {Colors.bold}Test Case: {test_num}{Colors.reset}")
    print(section)
    status_box = f"{color}{Colors.bold}{emoji} Status:{Colors.reset} "
    status_msg = f"[{color}{status}{Colors.reset}]"
    file_tag = f"{Colors.fg.lightgrey}({file_name}){Colors.reset}"
    print(f"{status_box} {status_msg}  {file_tag}")
    print(section)
    print(f"{Colors.fg.yellow}{Colors.bold}📥 Input:{Colors.reset}")
    print(sub_border)
    print(f"{Colors.fg.white}{input_data.strip()}{Colors.reset}")
    print(section)
    print(f"{Colors.fg.green}{Colors.bold}✅ Expected Output:{Colors.reset}")
    print(sub_border)
    print(f"{Colors.fg.white}{expected_output.strip()}{Colors.reset}")
    print(section)
    print(f"{Colors.fg.red}{Colors.bold}❌ Your Output:{Colors.reset}")
    print(sub_border)
    if your_output.strip():
        print(f"{Colors.fg.white}{your_output.strip()}{Colors.reset}")
    else:
        print(f"{Colors.fg.darkgrey}<no output>{Colors.reset}")
    print(border)

def stress_testing(test_cases=None, time_limit=None):
    try:
        if test_cases is None:
            test_cases = int(
                input(f"{Colors.fg.gold}Enter the number of test cases: {Colors.reset}")
            )
        if time_limit is None:
            time_limit = float(
                input(
                    f"{Colors.fg.gold}Enter the time limit for each test case (seconds): {Colors.reset}"
                )
            )
    except (ValueError, KeyboardInterrupt):
        print(f"\n{Colors.fg.red}Invalid input or interrupted. Exiting.{Colors.reset}")
        return

    print(f"{Colors.fg.white}\n=========================={Colors.reset}\n")

    list_of_files = ["generator", "correct", "test"]
    list_of_input_files = ["", "input.txt", "input.txt"]
    list_of_output_files = ["input.txt", "correct_output.txt", "test_output.txt"]

    # Compile all files first
    for file in list_of_files:
        try:
            cpp_compiler.compile_file(file_name=file)
        except ValueError as e:
            print(f"\n{Colors.fg.red}{e}{Colors.reset}")
            return

    for test in range(1, test_cases + 1):
        for index in range(len(list_of_files)):
            try:
                cpp_compiler.validate_errors(
                    list_of_files[index],
                    list_of_input_files[index],
                    list_of_output_files[index],
                    test,
                    time_limit,
                )
            except Exception as e:
                # Enhanced output for errors
                status = str(e)
                if "Time Limit Exceeded" in status:
                    status_text = "TIME LIMIT EXCEEDED"
                    status_color = Colors.fg.yellow
                elif "Wrong Answer" in status or "differs" in status:
                    status_text = "WRONG ANSWER"
                    status_color = Colors.fg.red
                elif "Runtime Error" in status:
                    status_text = "RUNTIME ERROR"
                    status_color = Colors.fg.magenta
                else:
                    status_text = "ERROR"
                    status_color = Colors.fg.red
                # Read input and outputs
                try:
                    with open("data/input.txt", "r") as f:
                        input_data = f.read()
                except Exception:
                    input_data = "<Could not read input.txt>"
                try:
                    with open("data/correct_output.txt", "r") as f:
                        expected_output = f.read()
                except Exception:
                    expected_output = "<Could not read correct_output.txt>"
                try:
                    with open("data/test_output.txt", "r") as f:
                        your_output = f.read()
                except Exception:
                    your_output = "<Could not read test_output.txt>"
                print_test_result(
                    test_num=test,
                    status=status_text,
                    status_color=status_color,
                    input_data=input_data,
                    expected_output=expected_output,
                    your_output=your_output,
                    file_name=list_of_files[index]+".cpp"
                )
                file_handler.clean_up()
                return

        if cpp_compiler.check_diff("correct_output.txt", "test_output.txt"):
            print(
                f"{Colors.fg.white}Test case {test} {Colors.fg.green}passed! ✅{Colors.reset}"
            )
        else:
            # Enhanced output for wrong answer
            try:
                with open("data/input.txt", "r") as f:
                    input_data = f.read()
            except Exception:
                input_data = "<Could not read input.txt>"
            try:
                with open("data/correct_output.txt", "r") as f:
                    expected_output = f.read()
            except Exception:
                expected_output = "<Could not read correct_output.txt>"
            try:
                with open("data/test_output.txt", "r") as f:
                    your_output = f.read()
            except Exception:
                your_output = "<Could not read test_output.txt>"
            print_test_result(
                test_num=test,
                status="WRONG ANSWER",
                status_color=Colors.fg.red,
                input_data=input_data,
                expected_output=expected_output,
                your_output=your_output,
                file_name="test.cpp"
            )
            file_handler.clean_up()
            return

    print(f"{Colors.fg.white}==========================\n{Colors.reset}")
    print(f"\n{Colors.fg.pink}All test cases {Colors.fg.green}passed! ✅{Colors.reset}")
    file_handler.clean_up()

def main():
    enable_windows_colors()
    parser = argparse.ArgumentParser(description="Stress Testing Tool")
    parser.add_argument('--tests', type=int, help='Number of test cases')
    parser.add_argument('--time', type=float, help='Time limit per test case (seconds)')
    args = parser.parse_args()
    stress_testing(test_cases=args.tests, time_limit=args.time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.fg.red}Interrupted by user. Exiting.{Colors.reset}")
        file_handler.clean_up()
