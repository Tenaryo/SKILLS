#!/usr/bin/env python3
"""Initialize or standardize a C++ project with the canonical project structure.

Usage:
    python3 init_cpp_project.py [--name PROJECT_NAME] [--author AUTHOR] [--path PATH]

If run inside an existing project directory, it will detect existing source files
and integrate them into the new structure. If run in an empty directory, it will
create a minimal hello-world scaffold.

Template placeholders ({{VAR}}) are replaced with actual values.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

PLACEHOLDER_MAP = {}


def detect_project_name(target_dir: Path) -> str:
    name = target_dir.resolve().name
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if not name:
        name = "my_project"
    return name


def to_lib_name(project_name: str) -> str:
    return project_name + "_core"


def collect_existing_sources(target_dir: Path) -> dict:
    src_files = []
    test_files = []
    other_cpp = []

    for p in target_dir.rglob("*.cpp"):
        rel = p.relative_to(target_dir)
        if any(part in rel.parts for part in ("build", ".git", "node_modules", "_deps")):
            continue
        name = p.name
        if name.startswith("test_") or name.startswith("test"):
            test_files.append(p)
        elif p.parent == target_dir and name in ("main.cpp",):
            src_files.append(p)
        elif p.parent == target_dir:
            other_cpp.append(p)
        else:
            other_cpp.append(p)

    hpp_files = []
    for p in target_dir.rglob("*.hpp"):
        rel = p.relative_to(target_dir)
        if any(part in rel.parts for part in ("build", ".git", "node_modules", "_deps")):
            continue
        hpp_files.append(p)

    h_files = []
    for p in target_dir.rglob("*.h"):
        rel = p.relative_to(target_dir)
        if any(part in rel.parts for part in ("build", ".git", "node_modules", "_deps")):
            continue
        h_files.append(p)

    return {
        "main": src_files,
        "tests": test_files,
        "other_cpp": other_cpp,
        "hpp": hpp_files,
        "h": h_files,
    }


def apply_template(content: str) -> str:
    for key, val in PLACEHOLDER_MAP.items():
        content = content.replace("{{" + key + "}}", val)
    return content


def write_template(asset_path: Path, target_path: Path) -> None:
    content = asset_path.read_text(encoding="utf-8")
    content = apply_template(content)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    print(f"  created: {target_path}")


def copy_asset_file(asset_rel: str, target_dir: Path, dest_name: str | None = None) -> None:
    src = ASSETS_DIR / asset_rel
    if not src.exists():
        print(f"  skipped (not found): {asset_rel}")
        return
    name = dest_name or src.name
    dst = target_dir / name
    write_template(src, dst)


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | 0o755)


def move_sources_to_src(target_dir: Path, sources: dict) -> None:
    src_dir = target_dir / "src"
    src_dir.mkdir(exist_ok=True)

    for f in sources.get("main", []):
        if f.parent != src_dir:
            dest = src_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                print(f"  moved: {f} -> {dest}")

    for f in sources.get("other_cpp", []):
        if f.parent != src_dir:
            dest = src_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                print(f"  moved: {f} -> {dest}")

    for f in sources.get("hpp", []):
        if f.parent != src_dir:
            dest = src_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                print(f"  moved: {f} -> {dest}")

    for f in sources.get("h", []):
        if f.parent != src_dir:
            dest = src_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                print(f"  moved: {f} -> {dest}")


def move_tests_to_tests(target_dir: Path, sources: dict) -> None:
    tests_dir = target_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    for f in sources.get("tests", []):
        if f.parent != tests_dir:
            dest = tests_dir / f.name
            if not dest.exists():
                shutil.move(str(f), str(dest))
                print(f"  moved: {f} -> {dest}")


def create_scaffold(target_dir: Path) -> None:
    src_dir = target_dir / "src"
    tests_dir = target_dir / "tests"
    src_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    main_cpp = src_dir / "main.cpp"
    if not main_cpp.exists():
        project_name = PLACEHOLDER_MAP["PROJECT_NAME"]
        lib_name = PLACEHOLDER_MAP["LIB_NAME"]
        main_content = apply_template(
            f'#include <iostream>\n\nauto main() -> int {{\n    std::cout << "Hello from {project_name}!" << std::endl;\n    return 0;\n}}\n'
        )
        main_cpp.write_text(main_content, encoding="utf-8")
        print(f"  created: {main_cpp}")

    test_main = tests_dir / "test_main.cpp"
    if not test_main.exists():
        test_content = apply_template(
            '#include <gtest/gtest.h>\n\nTEST(MainTest, SanityCheck) {\n    EXPECT_TRUE(true);\n}\n'
        )
        test_main.write_text(test_content, encoding="utf-8")
        print(f"  created: {test_main}")


def update_cmake_test_entries(target_dir: Path, sources: dict) -> None:
    tests_dir = target_dir / "tests"
    tests_cmake = tests_dir / "CMakeLists.txt"
    lib_name = PLACEHOLDER_MAP["LIB_NAME"]

    test_files = list(tests_dir.glob("test_*.cpp"))
    if not test_files:
        return

    lines = []
    for tf in sorted(test_files):
        name = tf.stem
        lines.append(f"add_executable({name} {name}.cpp)")
        lines.append(f"target_link_libraries({name} PRIVATE {lib_name} GTest::gtest_main)")
        lines.append(f"gtest_discover_tests({name})")
        lines.append("")

    tests_cmake.write_text("\n".join(lines), encoding="utf-8")
    print(f"  updated: {tests_cmake}")


def generate_readme(target_dir: Path) -> None:
    readme = target_dir / "README.md"
    if readme.exists():
        print(f"  skipped (exists): {readme}")
        return

    project_name = PLACEHOLDER_MAP["PROJECT_NAME"]
    content = f"""# {project_name}

A C++ project.

## Requirements

- C++23 compiler (GCC 13+ / Clang 17+)
- CMake 3.21+
- Ninja (recommended)

## Build

```sh
./build.sh            # Debug build (default)
./build.sh Release    # Release build
```

Or manually:

```sh
cmake -B build -S . -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j$(nproc)
```

### Sanitizers

Enable Address Sanitizer and Undefined Behavior Sanitizer:

```sh
cmake -B build -S . -G Ninja -DENABLE_SANITIZERS=ON
cmake --build build -j$(nproc)
```

## Test

```sh
./run_tests.sh
```

## Project Structure

```
src/
  main.cpp          # Entry point
tests/
  test_main.cpp     # Test suite
```

## License

See [LICENSE](LICENSE).
"""
    readme.write_text(content, encoding="utf-8")
    print(f"  created: {readme}")


def run(args: argparse.Namespace) -> None:
    target_dir = Path(args.path).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    project_name = args.name or detect_project_name(target_dir)
    lib_name = to_lib_name(project_name)
    author = args.author or "TODO"
    year = str(datetime.now().year)

    global PLACEHOLDER_MAP
    PLACEHOLDER_MAP = {
        "PROJECT_NAME": project_name,
        "LIB_NAME": lib_name,
        "AUTHOR": author,
        "YEAR": year,
    }

    print(f"\nInitializing C++ project: {project_name}")
    print(f"Library target: {lib_name}")
    print(f"Target directory: {target_dir}\n")

    sources = collect_existing_sources(target_dir)

    has_existing = bool(sources["main"] or sources["other_cpp"] or sources["hpp"] or sources["h"] or sources["tests"])

    if has_existing:
        print("Found existing source files, integrating into project structure...")
        move_sources_to_src(target_dir, sources)
        move_tests_to_tests(target_dir, sources)

    print("\nGenerating project files...")

    copy_asset_file("CMakeLists.txt", target_dir)
    copy_asset_file("build.sh", target_dir)
    copy_asset_file("run_tests.sh", target_dir)
    copy_asset_file(".clang-format", target_dir)
    copy_asset_file(".gitignore", target_dir)
    copy_asset_file(".gitattributes", target_dir)
    copy_asset_file("LICENSE", target_dir)

    copy_asset_file("tests_CMakeLists.txt", target_dir / "tests", "CMakeLists.txt")

    copy_asset_file(".github/workflows/ci.yml", target_dir / ".github" / "workflows")
    copy_asset_file(".github/PULL_REQUEST_TEMPLATE.md", target_dir / ".github")
    copy_asset_file(".github/ISSUE_TEMPLATE/bug_report.yml", target_dir / ".github" / "ISSUE_TEMPLATE")
    copy_asset_file(".github/ISSUE_TEMPLATE/config.yml", target_dir / ".github" / "ISSUE_TEMPLATE")
    copy_asset_file(".github/ISSUE_TEMPLATE/feature_request.yml", target_dir / ".github" / "ISSUE_TEMPLATE")
    copy_asset_file(".github/ISSUE_TEMPLATE/question.yml", target_dir / ".github" / "ISSUE_TEMPLATE")

    make_executable(target_dir / "build.sh")
    make_executable(target_dir / "run_tests.sh")

    if not has_existing:
        create_scaffold(target_dir)

    update_cmake_test_entries(target_dir, sources)

    generate_readme(target_dir)

    if not (target_dir / ".git").exists():
        print("\nInitializing git repository...")
        subprocess.run(["git", "init"], cwd=target_dir, check=True, capture_output=True)

    print(f"\nDone! Project '{project_name}' is ready at {target_dir}")
    print("\nNext steps:")
    print(f"  cd {target_dir}")
    print("  ./build.sh")
    print("  ./run_tests.sh")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a C++ project with canonical structure")
    parser.add_argument("--name", default=None, help="Project name (default: directory name)")
    parser.add_argument("--author", default=None, help="Author name for LICENSE")
    parser.add_argument("--path", default=".", help="Target directory (default: current)")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
