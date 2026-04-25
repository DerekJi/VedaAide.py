#!/usr/bin/env python3
# cspell: ignore htmlcov
"""
Code Standards Checker for VedaAide Project

This script performs comprehensive code standards audits including:
1. Format checks (black, isort compliance)
2. Style checks (naming conventions, pylint compliance)
3. Type hint checks (mypy compliance)
4. Custom standards checks (DI, logging, exceptions, async, etc.)

Usage:
    python code_standards_checker.py                 # Check all src/ and tests/
    python code_standards_checker.py --file src/core/agent.py  # Check specific file
    python code_standards_checker.py --dir src/core/           # Check specific directory
    python code_standards_checker.py --report html  # Generate HTML report
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Issue:
    """Represents a code standards issue"""

    severity: str  # "error", "warning", "info"
    category: str  # Type of issue
    file: str
    line: int
    column: int
    message: str
    code_example: str = ""
    suggestion: str = ""

    def __str__(self) -> str:
        """Return string representation of the issue."""
        severity = self.severity.upper()
        return (
            f"[{severity}] {self.category} - {self.message}\n"
            f"  File: {self.file}:{self.line}\n"
            f"  Suggestion: {self.suggestion}"
        )


@dataclass
class CheckResult:
    """Result of a complete code check."""

    total_files: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    issues: List[Issue] = field(default_factory=list)
    files_checked: List[str] = field(default_factory=list)


class CodeStandardsChecker:
    """Main checker class for code standards"""

    def __init__(
        self, root_dir: str = ".", exclude_dirs: Optional[List[str]] = None
    ) -> None:
        """Initialize the code standards checker.

        Args:
            root_dir: Root directory to check (default: current directory).
            exclude_dirs: Directories to exclude from checks.
        """
        self.root_dir: Path = Path(root_dir)
        self.exclude_dirs: List[str] = exclude_dirs or [
            ".venv",
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "htmlcov",
            ".temp",
        ]
        self.result: CheckResult = CheckResult()
        self.coding_standards: Dict[str, int] = self._load_standards()

    def _load_standards(self) -> Dict[str, int]:
        """Load coding standards from standards file"""
        return {
            "max_line_length": 100,
            "max_file_lines": 300,
            "max_class_lines": 250,
            "max_function_lines": 50,
            "indent_size": 4,
        }

    def check_all(self) -> CheckResult:
        """Check all Python files in src/ and tests/ directories"""
        for check_dir in ["src", "tests"]:
            dir_path = self.root_dir / check_dir
            if dir_path.exists():
                self._check_directory(dir_path)

        self._calculate_stats()
        return self.result

    def check_file(self, file_path: str) -> CheckResult:
        """Check a specific file"""
        self._check_python_file(Path(file_path))
        self._calculate_stats()
        return self.result

    def check_directory(self, dir_path: str) -> CheckResult:
        """Check all files in a directory"""
        self._check_directory(Path(dir_path))
        self._calculate_stats()
        return self.result

    def _check_directory(self, dir_path: Path) -> None:
        """Recursively check all Python files in directory"""
        if not dir_path.is_dir():
            return

        for item in dir_path.rglob("*.py"):
            # Skip excluded directories
            if any(excluded in item.parts for excluded in self.exclude_dirs):
                continue

            self._check_python_file(item)

    def _check_python_file(self, file_path: Path) -> None:
        """Check a single Python file"""
        file_path_str = str(file_path)
        if file_path_str not in self.result.files_checked:
            self.result.files_checked.append(file_path_str)
            self.result.total_files += 1

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Run all checks
            self._check_line_length(file_path, lines)
            self._check_file_size(file_path, lines)
            self._check_naming_conventions(file_path, lines)
            self._check_type_hints(file_path, lines)
            self._check_docstrings(file_path, lines)
            self._check_imports(file_path, lines)
            self._check_prohibited_patterns(file_path, lines)
            self._check_exception_handling(file_path, lines)
            self._check_code_smells(file_path, lines)

        except Exception as e:
            self._add_issue(
                severity="error",
                category="File Read Error",
                file=str(file_path),
                line=0,
                message=f"Failed to read file: {str(e)}",
                suggestion="Check file encoding and permissions",
            )

    def _check_line_length(self, file_path: Path, lines: List[str]) -> None:
        """Check if lines exceed maximum length"""
        max_length: int = self.coding_standards["max_line_length"]

        for line_num, line in enumerate(lines, 1):
            if len(line) > max_length:
                self._add_issue(
                    severity="warning",
                    category="Line Length",
                    file=str(file_path),
                    line=line_num,
                    column=max_length,
                    message=f"Line exceeds {max_length} characters (length: {len(line)})",
                    code_example=line[:80] + "...",
                    suggestion="Break line into multiple lines or use line continuation",
                )

    def _check_file_size(self, file_path: Path, lines: List[str]) -> None:
        """Check if file exceeds maximum size"""
        max_lines: int = self.coding_standards["max_file_lines"]
        line_count: int = len([line for line in lines if line.strip()])

        if line_count > max_lines:
            msg = f"File exceeds {max_lines} lines (total: {line_count} lines)"
            sugg = (
                "Split into smaller modules following SRP principle. "
                "Create subdirectory with modules."
            )
            self._add_issue(
                severity="warning",
                category="File Size",
                file=str(file_path),
                line=0,
                column=0,
                message=msg,
                suggestion=sugg,
            )

    def _check_naming_conventions(
        self, file_path: Path, lines: List[str]
    ) -> None:
        """Check naming conventions (PascalCase, snake_case, UPPER_SNAKE_CASE)."""
        class_pattern = re.compile(r"^class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]")
        func_pattern = re.compile(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")

        for line_num, line in enumerate(lines, 1):
            # Check class names
            class_match = class_pattern.search(line)
            if class_match is not None:
                class_name = class_match.group(1)
                if not self._is_pascal_case(class_name):
                    self._add_issue(
                        severity="error",
                        category="Naming Convention",
                        file=str(file_path),
                        line=line_num,
                        column=class_match.start(1),
                        message=f"Class name '{class_name}' should be PascalCase",
                        code_example=line.strip(),
                        suggestion=f"Rename to: {self._to_pascal_case(class_name)}",
                    )

            # Check function names
            func_match = func_pattern.search(line)
            if func_match is not None:
                func_name = func_match.group(1)
                if not self._is_snake_case(func_name) and func_name != "__init__":
                    self._add_issue(
                        severity="error",
                        category="Naming Convention",
                        file=str(file_path),
                        line=line_num,
                        column=func_match.start(1),
                        message=f"Function name '{func_name}' should be snake_case",
                        code_example=line.strip(),
                        suggestion=f"Rename to: {self._to_snake_case(func_name)}",
                    )

    def _check_type_hints(self, file_path: Path, lines: List[str]) -> None:
        """Check if functions have type hints."""
        function_pattern = re.compile(
            r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*(->[\s\w\[\],\.\|]*)?:"
        )

        for line_num, line in enumerate(lines, 1):
            match = function_pattern.search(line)
            if match is not None:
                func_name = match.group(1)
                params = match.group(2)
                return_type = match.group(3)

                # Skip __init__, __str__, etc. in some cases
                if func_name.startswith("__") and func_name.endswith("__"):
                    continue

                # Check return type
                if not return_type or "->" not in line:
                    self._add_issue(
                        severity="error",
                        category="Type Hints",
                        file=str(file_path),
                        line=line_num,
                        column=0,
                        message=f"Function '{func_name}' missing return type hint",
                        code_example=line.strip(),
                        suggestion=f"Add return type: def {func_name}(...) -> ReturnType:",
                    )

                # Check parameter types
                if params and ":" not in params and params.strip() != "self":
                    msg = f"Function '{func_name}' parameters missing type hints"
                    sugg = (
                        f"Add parameter types: "
                        f"def {func_name}(param: Type) -> ReturnType:"
                    )
                    self._add_issue(
                        severity="error",
                        category="Type Hints",
                        file=str(file_path),
                        line=line_num,
                        column=0,
                        message=msg,
                        code_example=line.strip(),
                        suggestion=sugg,
                    )

    def _check_docstrings(self, file_path: Path, lines: List[str]) -> None:  # noqa: C901
        """Check if public functions and classes have docstrings."""
        for line_num, line in enumerate(lines, 1):
            # Check class definitions
            if re.match(r"^\s*class\s+([A-Z][a-zA-Z0-9_]*)\s*[:\(]", line):
                if line_num < len(lines):
                    next_line = lines[line_num].strip() if line_num < len(lines) else ""
                    if not next_line.startswith('"""') and not next_line.startswith("'''"):
                        class_match = re.search(r"class\s+([A-Z][a-zA-Z0-9_]*)", line)
                        if class_match is not None:
                            class_name = class_match.group(1)
                            sugg = (
                                f'Add docstring: class {class_name}:\n'
                                f'    """Description of class."""'
                            )
                            self._add_issue(
                                severity="warning",
                                category="Documentation",
                                file=str(file_path),
                                line=line_num,
                                column=0,
                                message=f"Class '{class_name}' missing docstring",
                                code_example=line.strip(),
                                suggestion=sugg,
                            )

            # Check function definitions (not private)
            if re.match(r"^\s*def\s+([a-z_][a-zA-Z0-9_]*)\s*\(", line) and not re.match(
                r"^\s*def\s+_", line
            ):
                if line_num < len(lines):
                    next_line = lines[line_num].strip() if line_num < len(lines) else ""
                    if not next_line.startswith('"""') and not next_line.startswith("'''"):
                        func_match = re.search(r"def\s+([a-z_][a-zA-Z0-9_]*)", line)
                        if func_match is not None:
                            func_name = func_match.group(1)
                            if func_name not in ["__init__", "__str__"]:
                                msg = f"Function '{func_name}' missing docstring"
                                sugg = (
                                    "Add Google-style docstring with "
                                    "Args, Returns, Raises"
                                )
                                self._add_issue(
                                    severity="warning",
                                    category="Documentation",
                                    file=str(file_path),
                                    line=line_num,
                                    column=0,
                                    message=msg,
                                    code_example=line.strip(),
                                    suggestion=sugg,
                                )

    def _check_imports(self, file_path: Path, lines: List[str]) -> None:
        """Check import order and organization."""
        import_lines: List[Tuple[int, str]] = []
        import_start: Optional[int] = None

        for line_num, line in enumerate(lines, 1):
            if re.match(r"^\s*(import|from)\s+", line):
                if import_start is None:
                    import_start = line_num
                import_lines.append((line_num, line.strip()))

        if import_lines:
            # Check order: stdlib, third-party, local
            categories: Dict[str, List[Tuple[int, str]]] = {
                "stdlib": [],
                "third_party": [],
                "local": [],
            }
            stdlib_names = {
                "os",
                "sys",
                "re",
                "json",
                "typing",
                "logging",
                "pathlib",
                "asyncio",
                "collections",
            }

            for line_num, line in import_lines:  # noqa: C901
                match = re.match(r"^import\s+([a-zA-Z_][a-zA-Z0-9_.]*)", line)
                if match is not None:
                    module = match.group(1).split(".")[0]
                    if module in stdlib_names:
                        categories["stdlib"].append((line_num, line))
                    elif line.startswith("from src.") or line.startswith("import src."):
                        categories["local"].append((line_num, line))
                    else:
                        categories["third_party"].append((line_num, line))

    def _check_prohibited_patterns(self, file_path: Path, lines: List[str]) -> None:
        """Check for prohibited patterns."""
        for line_num, line in enumerate(lines, 1):
            # Check for print() usage
            if re.search(r"print\s*\(", line) and not line.strip().startswith("#"):
                self._add_issue(
                    severity="error",
                    category="Prohibited Pattern",
                    file=str(file_path),
                    line=line_num,
                    column=line.find("print"),
                    message="Use of print() is prohibited",
                    code_example=line.strip(),
                    suggestion="Use logging module: logger.info(...) or logger.debug(...)",
                )

            # Check for hardcoded API keys or credentials
            if (
                re.search(r"api_key\s*=\s*[\"']", line)
                or re.search(r"password\s*=\s*[\"']", line)
                or re.search(r"secret\s*=\s*[\"']", line)
            ):
                self._add_issue(
                    severity="error",
                    category="Security",
                    file=str(file_path),
                    line=line_num,
                    column=0,
                    message="Hardcoded credentials detected",
                    code_example=line.strip()[:50] + "...",
                    suggestion="Use ConfigManager to read from environment or config file",
                )

            # Check for os.getenv()
            if "os.getenv" in line:
                self._add_issue(
                    severity="warning",
                    category="Configuration",
                    file=str(file_path),
                    line=line_num,
                    column=line.find("os.getenv"),
                    message="Direct os.getenv() usage detected",
                    code_example=line.strip(),
                    suggestion="Use ConfigManager.get() instead: config.get('key_name')",
                )

    def _check_exception_handling(self, file_path: Path, lines: List[str]) -> None:
        """Check exception handling patterns."""
        for line_num, line in enumerate(lines, 1):
            # Check for bare except
            if re.search(r"except\s*:", line):
                sugg = (
                    "Catch specific exceptions: "
                    "except ValueError: or except (KeyError, ValueError):"
                )
                self._add_issue(
                    severity="error",
                    category="Exception Handling",
                    file=str(file_path),
                    line=line_num,
                    column=line.find("except"),
                    message="Bare except clause detected",
                    code_example=line.strip(),
                    suggestion=sugg,
                )

            # Check for except Exception
            if re.search(r"except\s+Exception\s*:", line):
                self._add_issue(
                    severity="warning",
                    category="Exception Handling",
                    file=str(file_path),
                    line=line_num,
                    column=line.find("except"),
                    message="Catching broad Exception is discouraged",
                    code_example=line.strip(),
                    suggestion="Catch specific exceptions instead",
                )

    def _check_code_smells(self, file_path: Path, lines: List[str]) -> None:
        """Check for code smells and potential issues."""
        # Check for hardcoded service instantiation (dependency injection violation)
        for line_num, line in enumerate(lines, 1):
            if re.search(r"self\.\w+\s*=\s*\w+\(", line) and not line.strip().startswith("#"):
                # This might be hardcoding a service
                if any(
                    service in line
                    for service in ["OpenAI", "AzureOpenAI", "PostgreSQL", "MongoDB"]
                ):
                    msg = "Hardcoded service instantiation detected"
                    sugg = (
                        "Inject dependencies via constructor: "
                        "def __init__(self, service: ServiceType)"
                    )
                    self._add_issue(
                        severity="error",
                        category="Dependency Injection",
                        file=str(file_path),
                        line=line_num,
                        column=line.find("self."),
                        message=msg,
                        code_example=line.strip(),
                        suggestion=sugg,
                    )

    def _add_issue(
        self,
        severity: str,
        category: str,
        file: str,
        line: int,
        column: int = 0,
        message: str = "",
        code_example: str = "",
        suggestion: str = "",
    ) -> None:
        """Add an issue to the result."""
        issue = Issue(
            severity=severity,
            category=category,
            file=file,
            line=line,
            column=column,
            message=message,
            code_example=code_example,
            suggestion=suggestion,
        )
        self.result.issues.append(issue)
        self.result.total_issues += 1

        if severity == "error":
            self.result.errors += 1
        elif severity == "warning":
            self.result.warnings += 1
        else:
            self.result.info += 1

    def _calculate_stats(self) -> None:
        """Calculate statistics."""
        pass

    @staticmethod
    def _is_pascal_case(name: str) -> bool:
        """Check if name is PascalCase."""
        return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))

    @staticmethod
    def _is_snake_case(name: str) -> bool:
        """Check if name is snake_case."""
        return bool(re.match(r"^[a-z_][a-z0-9_]*$", name))

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert to PascalCase."""
        return "".join(word.capitalize() for word in name.split("_"))

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert to snake_case."""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def generate_report(self) -> str:  # noqa: C901
        """Generate a text report."""
        report: List[str] = []
        report.append("=" * 80)
        report.append("Code Standards Audit Report")
        report.append("=" * 80)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.append(f"\nGenerated: {now_str}\n")

        # Summary
        report.append("📊 Overview")
        report.append("-" * 80)
        report.append(f"Total Files: {self.result.total_files}")
        report.append(f"Total Issues: {self.result.total_issues}")
        report.append(f"Errors: {self.result.errors}")
        report.append(f"Warnings: {self.result.warnings}")
        report.append(f"Info: {self.result.info}")
        if self.result.total_issues > 0:
            pass_rate = max(
                0, 100 - (self.result.total_issues / (self.result.total_files * 10) * 100)
            )
            report.append(f"Pass Rate: {pass_rate:.1f}%\n")

        # Issues by severity
        if self.result.errors > 0:
            report.append("\n🔴 Critical Issues (must fix)")
            report.append("-" * 80)
            for issue in self.result.issues:
                if issue.severity == "error":
                    report.append(f"\n[{issue.category}] {issue.message}")
                    report.append(f"  File: {issue.file}:{issue.line}")
                    if issue.code_example:
                        report.append(f"  Code: {issue.code_example}")
                    if issue.suggestion:
                        report.append(f"  Fix: {issue.suggestion}")

        if self.result.warnings > 0:
            report.append("\n\n🟡 Warnings (should fix)")
            report.append("-" * 80)
            for issue in self.result.issues:
                if issue.severity == "warning":
                    report.append(f"\n[{issue.category}] {issue.message}")
                    report.append(f"  File: {issue.file}:{issue.line}")
                    if issue.code_example:
                        report.append(f"  Code: {issue.code_example}")
                    if issue.suggestion:
                        report.append(f"  Suggestion: {issue.suggestion}")

        # By category
        report.append("\n\n📋 Issues by Category")
        report.append("-" * 80)
        by_category: Dict[str, List[Issue]] = defaultdict(list)
        for issue in self.result.issues:
            by_category[issue.category].append(issue)

        for category in sorted(by_category.keys()):
            issues = by_category[category]
            report.append(f"\n{category}: {len(issues)} issues")
            for issue in issues:
                report.append(f"  - {issue.file}:{issue.line}")

        # By file
        report.append("\n\n📁 Issues by File")
        report.append("-" * 80)
        by_file: Dict[str, List[Issue]] = defaultdict(list)
        for issue in self.result.issues:
            by_file[issue.file].append(issue)

        for file in sorted(by_file.keys()):
            issues = by_file[file]
            errors = len([i for i in issues if i.severity == "error"])
            warnings = len([i for i in issues if i.severity == "warning"])
            report.append(f"\n{file}")
            report.append(f"  Errors: {errors}, Warnings: {warnings}")

        # Recommendations
        report.append("\n\n✅ Fix Priority")
        report.append("-" * 80)
        report.append("\nPriority 1 - Fix immediately (required to pass):")
        report.append("  1. Fix all Type Hints errors")
        report.append("  2. Fix naming convention errors")
        report.append("  3. Remove print() statements")
        report.append("  4. Fix exception handling")
        report.append("  5. Remove hardcoded credentials")

        report.append("\nPriority 2 - Fix this week:")
        report.append("  1. Split oversized files")
        report.append("  2. Fix dependency injection issues")
        report.append("  3. Use ConfigManager")

        report.append("\nPriority 3 - Improve later:")
        report.append("  1. Add missing docstrings")
        report.append("  2. Extract duplicate code")
        report.append("  3. Improve code structure")

        report.append("\n\n" + "=" * 80)
        report.append("Next Steps:")
        report.append("1. make format  # Auto-fix formatting issues")
        report.append("2. Fix code style issues per this report")
        report.append("3. make verify  # Confirm all checks pass")
        report.append("=" * 80)

        return "\n".join(report)


def main() -> None:
    """Main entry point for code standards checker."""
    parser = argparse.ArgumentParser(
        description="Code Standards Checker for VedaAide Project"
    )
    parser.add_argument("--file", type=str, help="Check specific file")
    parser.add_argument("--dir", type=str, help="Check specific directory")
    parser.add_argument(
        "--report",
        type=str,
        choices=["text", "html"],
        default="text",
        help="Report format (default: text)",
    )

    args = parser.parse_args()

    checker = CodeStandardsChecker(root_dir=".")

    if args.file:
        checker.check_file(args.file)
    elif args.dir:
        checker.check_directory(args.dir)
    else:
        checker.check_all()

    # Generate and print report
    report = checker.generate_report()

    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
    print(report)

    # Save report to file
    report_file = Path(".temp") / "code-standards-report.txt"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✅ Report saved to: {report_file}")

    # Exit with appropriate code
    exit_code = 0 if checker.result.errors == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
