# Stress Testing

## Overview

Stress Testing is a tool for competitive programming and algorithm development that helps you verify the correctness and efficiency of your C++ solutions by comparing them against a brute-force solution on randomly generated test cases.

## Features
- Modular, extensible C++ test case generators (arrays, graphs, strings, numbers, etc.)
- Cross-platform: works on macOS, Linux, and Windows
- Flexible: set number of test cases and time limit via CLI or prompt
- Clear output for Accepted, Wrong Answer, Time Limit Exceeded, and Runtime Error
- Easy to extend with your own generators and solutions

## Requirements
- Python 3
- g++ (or g++-13 on macOS; can be set via the `CXX` environment variable)
- CMake (optional, for building with CMake)

## Installation Requirements

### Python 3
- macOS: Pre-installed, or install via Homebrew:
  ```sh
  brew install python3
  ```
- Linux (Debian/Ubuntu):
  ```sh
  sudo apt update && sudo apt install python3 python3-pip
  ```
- Windows: [Download Python](https://www.python.org/downloads/) and add to PATH.

### C++ Compiler
- macOS: Install Xcode Command Line Tools:
  ```sh
  xcode-select --install
  ```
- Linux (Debian/Ubuntu):
  ```sh
  sudo apt update && sudo apt install build-essential g++
  ```
- Windows: Install [MinGW-w64](http://mingw-w64.org/doku.php/download) or use [WSL](https://docs.microsoft.com/en-us/windows/wsl/).

### CMake (Optional, for CMake builds)
- macOS:
  ```sh
  brew install cmake
  ```
- Linux:
  ```sh
  sudo apt install cmake
  ```
- Windows: [Download CMake](https://cmake.org/download/) and add to PATH.

## Installation
```bash
git clone https://github.com/7oSkaaa/stress_testing.git
cd stress_testing
```

## Folder Structure
```
📦 Stress_Testing
├── 📄 CMakeLists.txt
├── 📄 README.md
├── 🐍 stress_testing.py
├── 🗂️ build/
│   ├── 📄 cmake_install.cmake
│   ├── 📄 CMakeCache.txt
│   ├── ⚙️  Makefile
│   ├── 🗂️ CMakeFiles/
│   │   ├── ...
│   ├── ⚙️  correct
│   ├── ⚙️  generator
│   ├── ⚙️  test
│   └── ...
├── 🗂️ cpp/
│   ├── 📄 correct.cpp
│   ├── 📄 generator.cpp
│   ├── 📄 test.cpp
│   └── 🗂️ generators/
│       ├── 📄 generator_arrays.h
│       ├── 📄 generator_graphs.h
│       ├── 📄 generator_numbers.h
│       ├── 📄 generator_strings.h
│       └── 📄 generator_utils.h
├── 🗂️ data/
│   ├── 📄 correct_output.txt
│   ├── 📄 input.txt
│   └── 📄 test_output.txt
├── 🗂️ src/
│   ├── 📄 __init__.py
│   └── 🗂️ utils/
│       ├── 📄 __init__.py
│       ├── 📄 cpp_compiler.py
│       ├── 📄 file_handler.py
│       └── 📄 terminal_colors.py
└── ...
```

## How to Use

### 1. Prepare Your Solutions
- Place your brute-force solution in `cpp/correct.cpp`.
- Place your optimized solution in `cpp/test.cpp`.
- Edit `cpp/generator.cpp` to generate test cases using the modular generators from `cpp/generators/`.

### 2. Generate Test Cases
Edit `generator.cpp` to use the flexible generators. Example:
```cpp
#include "generators/generator_numbers.h"
#include "generators/generator_arrays.h"
#include "generators/generator_strings.h"
#include "generators/generator_graphs.h"
#include "generators/generator_utils.h"

int main() {
    std::mt19937_64 rng(std::chrono::steady_clock::now().time_since_epoch().count());
    int n = gen_numbers::random<int>(5, 15, rng);
    auto arr = gen_arrays::random<int>(n, 1, 100, rng);
    gen_utils::print(arr);
    auto s = gen_strings::random(n, gen_strings::CaseType::Lower, rng);
    std::cout << s << '\n';
    auto tree = gen_graphs::tree(n, rng);
    gen_utils::print(tree);
    // ... more generators ...
    return 0;
}
```

### 3. Build the C++ Files
#### Option 1: Using Python Script (Recommended)
The script will compile everything for you.

#### Option 2: Using CMake (Optional)
```bash
cmake -S . -B build
cmake --build build
```
This will create executables for generator, test, and correct in the build directory.

### 4. Run the Stress Test
You can run the stress test from the terminal or an IDE:

```bash
python stress_testing.py --tests 100 --time 2
```
- `--tests` (optional): Number of test cases (if not provided, you will be prompted)
- `--time` (optional): Time limit per test case in seconds (if not provided, you will be prompted)

### 5. Output
- **Accepted**: Your solution matches the brute-force output.
- **Wrong Answer**: Shows the input, expected output, and your output for the failed test case.
- **Time Limit Exceeded**: Your solution exceeded the time limit.
- **Runtime Error**: Your solution crashed.

## C++ Generator Libraries Reference

### generator_numbers.h
- `random < T > (T l, T r, rng)`: Random integer in [l, r].
- `random_range < T > (T l, T r, int count, rng)`: Vector of random integers in [l, r].
- `random_exclude < T > (T l, T r, set < T > exclude, rng)`: Random integer in [l, r] not in exclude.
- `random_range_exclude < T > (T l, T r, int count, set < T > exclude, rng)`: Vector of random integers not in exclude.
- `random_weighted < T > (vector < T > values, vector < double > weights, rng)`: Random value from values with custom weights.
- `random_real < T > (T l, T r, rng)`: Random floating-point in [l, r].
- `random_real_exclude < T > (T l, T r, T excl_l, T excl_r, rng)`: Random real in [l, r] excluding [excl_l, excl_r].

### generator_arrays.h
- `random < T > (int len, T l, T r, rng, unique, sorted)`: Random array of length len in [l, r].
- `permutation < T > (int n, rng)`: Random permutation of 1..n.
- `matrix < T > (int rows, int cols, T l, T r, rng, unique_rows, sorted_rows)`: 2D array.
- `pairs < T > (int len, T l1, T r1, T l2, T r2, rng, ordered)`: Vector of pairs.
- `subset < T > (T l, T r, int k, rng, sorted)`: Unique subset of size k from [l, r].
- `partition < T > (T sum, int k, T min_val, T max_val, rng)`: Partition sum into k parts.
- `arithmetic_progression < T > (int len, T start, T step)`: Arithmetic progression.
- `geometric_progression < T > (int len, T start, T ratio)`: Geometric progression.
- `constant_array < T > (int len, T value)`: Array with all elements equal.
- `bit_array < T > (int len, double prob_one, rng)`: Bit array (0/1) with probability for 1s.
- `shuffled < T > (vector < T > v, rng)`: Shuffled copy of v.
- `strictly_increasing < T > (int len, T start, T step_min, T step_max, rng)`: Strictly increasing array.
- `strictly_decreasing < T > (int len, T start, T step_min, T step_max, rng)`: Strictly decreasing array.
- `random_with_sum < T > (int len, T sum, T min_val, T max_val, rng)`: Random array with given sum.

### generator_strings.h
- `random (int len, CaseType, rng, char l, char r)`: Random string.
- `palindrome (int len, CaseType, rng, char l, char r)`: Palindrome string.
- `random_alphanum (int len, bool letters, bool digits, CaseType, rng)`: Alphanumeric string.
- `random_custom (int len, string alphabet, rng)`: String from custom alphabet.
- `random_strings (int count, int len, CaseType, rng)`: Vector of random strings.
- `palindromes (int count, int len, CaseType, rng)`: Vector of palindromes.

### generator_graphs.h
- `tree (int n, rng)`: Random tree (edges).
- `simple_graph (int n, int m, rng)`: Simple connected graph.
- `weighted_graph (int n, int m, int min_w, int max_w, rng)`: Weighted graph.
- `directed_graph (int n, int m, rng)`: Directed graph.
- `dag (int n, int m, rng)`: Directed acyclic graph.
- `bipartite (int n1, int n2, int m, rng)`: Bipartite graph.
- `star (int n, rng, int center)`: Star graph.
- `cycle (int n, rng)`: Cycle graph.
- `complete (int n)`: Complete graph.
- `regular (int n, int d, rng)`: Regular graph.
- `tree_with_diameter (int n, int diameter, rng)`: Tree with given diameter.
- `chain_tree (int n)`: Chain tree (path).

### generator_utils.h
- `print (const vector < T > &v)`: Print vector.
- `print (const vector < pair < T, U > > &v)`: Print vector of pairs.
- `print (const vector < vector < T > > &mat)`: Print 2D vector.
- `print (const vector < tuple < Args... > > &v)`: Print vector of tuples.
- `print (const T &val)`: Print single value.
- `print (const vector < string > &v)`: Print vector of strings.

---

Each function is documented in the header files with parameter and return type. For more details, see the comments in each header.

## Notes
- The C++ compiler can be set via the `CXX` environment variable. On macOS, the script will use `g++-13` if available, otherwise `g++`.
- All generators and scripts are cross-platform and tested on macOS, Linux, and Windows.
- The project is modular and easy to extend for your own needs.
