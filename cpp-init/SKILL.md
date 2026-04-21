---
name: cpp-init
description: This skill should be used when the user asks to "initialize a C++ project", "create a C++ project", "set up a C++ project", "standardize a C++ codebase", "add CMake to my project", "add build system", "init cpp", "初始化C++项目", "规范化C++项目", or wants to scaffold or restructure a C++ project with a canonical build system, test infrastructure, CI, and project layout.
---

# cpp-init

Initialize or standardize a C++ project with a canonical structure: CMake build system, test runner, clang-format, CI pipeline, and GitHub templates.

## Quick Start

Run the initialization script:

```bash
python3 scripts/init_cpp_project.py --name PROJECT_NAME --author "Author Name" --path /target/directory
```

The script handles two scenarios:
1. **New project**: Creates a minimal hello-world scaffold with all project files
2. **Existing project**: Detects existing `.cpp`/`.hpp` files, moves them into `src/` and `tests/`, generates all infrastructure files around them

## What Gets Generated

### Core Files
- `CMakeLists.txt` — Root CMake config (C++23, INTERFACE library, strict warnings, sanitizer option, Google Test via FetchContent)
- `src/main.cpp` — Entry point (new projects only)
- `build.sh` — Build wrapper (Ninja + cmake)
- `run_tests.sh` — Test runner via ctest with colored output
- `.clang-format` — Code formatting (LLVM-based, 4-space indent, 100 columns)
- `.gitignore` — Build artifacts, CMake, IDE files
- `.gitattributes` — Line ending normalization
- `LICENSE` — MIT License
- `README.md` — Standard project documentation

### Test Infrastructure
- `tests/CMakeLists.txt` — Auto-discovers `test_*.cpp` files, one executable per file, linked with Google Test
- `tests/test_main.cpp` — Minimal test with Google Test (new projects only)

### GitHub Templates
- `.github/workflows/ci.yml` — Build + test + format check
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/question.yml`

## Workflow

### Scenario A: New Project from Scratch

1. Run `init_cpp_project.py` in an empty or new directory
2. The script creates the full scaffold with a hello-world `main.cpp` and a passing `test_main.cpp`
3. Git repository is initialized automatically
4. Run `./build.sh && ./run_tests.sh` to verify

### Scenario B: Existing Project Needs Structuring

1. Run `init_cpp_project.py` in the project root (or specify `--path`)
2. The script detects existing `.cpp`/`.hpp` files
3. Source files are moved to `src/`, test files (prefixed with `test_`) are moved to `tests/`
4. All infrastructure files are generated around the existing code
5. `tests/CMakeLists.txt` is updated to reference all discovered test files
6. Existing files (README.md, LICENSE, etc.) are NOT overwritten

### Scenario C: Adding Infrastructure to an Already-Structured Project

1. Run `init_cpp_project.py` in the project root
2. Files that already exist (e.g., `CMakeLists.txt`, `README.md`) are overwritten with templates — review changes carefully
3. Source and test files already in `src/` and `tests/` are left in place

## Key Conventions

Read `references/conventions.md` for the full specification. Key points:

- **C++23**, GCC 13+, CMake 3.21+, Ninja
- **INTERFACE library** (`{project}_core`) for shared compile options and includes
- **Strict warnings**: `-Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion`
- **Google Test** — fetched via CMake FetchContent (v1.14.0), no manual install needed
- **One test executable per `test_*.cpp` file** in `tests/`, discovered via `gtest_discover_tests`
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `build:`, `ci:`

## Template Placeholders

Asset files use `{{PLACEHOLDER}}` syntax, replaced by the init script:

| Placeholder | Description | Default |
|---|---|---|
| `{{PROJECT_NAME}}` | Project and executable name | Directory name |
| `{{LIB_NAME}}` | INTERFACE library name | `{project}_core` |
| `{{AUTHOR}}` | Author for LICENSE | "TODO" |
| `{{YEAR}}` | Copyright year | Current year |

## Resources

### scripts/
- **`init_cpp_project.py`** — Main initialization script. Detects existing code, generates all project files, initializes git. Run with `--help` for options.

### references/
- **`conventions.md`** — Full specification of project conventions: CMake patterns, build script behavior, test file conventions, CI pipeline, commit message format, code style rules.

### assets/
Template files copied to the target project. All use `{{PLACEHOLDER}}` syntax for substitution:
- `CMakeLists.txt` — Root CMake
- `tests_CMakeLists.txt` — Tests subdirectory CMake (copied as `tests/CMakeLists.txt`)
- `build.sh`, `run_tests.sh` — Shell scripts
- `.clang-format`, `.gitignore`, `.gitattributes` — Config files
- `LICENSE` — MIT License template
- `.github/` — CI workflow, issue/PR templates
