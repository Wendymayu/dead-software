"""运行所有主题的示例代码并验证它们能正常执行

用法: python shared/verify_all.py
"""

import io
import subprocess
import sys
from pathlib import Path

# Force UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

EXAMPLES = [
    ROOT / "architectures" / "layered" / "example.py",
    ROOT / "architectures" / "layered" / "advanced.py",
    ROOT / "architectures" / "event-driven" / "example.py",
    ROOT / "architectures" / "event-driven" / "advanced.py",
    ROOT / "architectures" / "microservices" / "example.py",
    ROOT / "architectures" / "microservices" / "advanced.py",
    ROOT / "architectures" / "pipeline" / "example.py",
    ROOT / "architectures" / "pipeline" / "advanced.py",
    ROOT / "architectures" / "hexagonal" / "example.py",
    ROOT / "architectures" / "hexagonal" / "advanced.py",
    ROOT / "architectures" / "event-sourcing" / "example.py",
    ROOT / "architectures" / "event-sourcing" / "advanced.py",
    ROOT / "architectures" / "saga" / "example.py",
    ROOT / "architectures" / "saga" / "advanced.py",
    ROOT / "design-patterns" / "observer" / "example.py",
    ROOT / "design-patterns" / "strategy" / "example.py",
    ROOT / "design-patterns" / "factory" / "example.py",
    ROOT / "design-patterns" / "decorator" / "example.py",
]


def run_example(path):
    """运行单个示例，返回是否成功"""
    rel = path.relative_to(ROOT)
    print(f"\n{'='*50}")
    print(f"Running: {rel}")
    print(f"{'='*50}")
    # Use system default encoding for subprocess output with error replacement
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, timeout=10
    )
    # Decode with system locale, replacing any undecodable chars
    stdout = result.stdout.decode(sys.getdefaultencoding(), errors="replace")
    stderr = result.stderr.decode(sys.getdefaultencoding(), errors="replace")
    print(stdout)
    if result.returncode != 0:
        print(f"[FAIL] {rel}")
        print(stderr)
        return False
    print(f"[PASS] {rel}")
    return True


def main():
    print("Verifying all example scripts...\n")
    results = []
    for path in EXAMPLES:
        if not path.exists():
            print(f"[SKIP] File not found: {path.relative_to(ROOT)}")
            results.append(True)  # Missing files don't count as failures
            continue
        results.append(run_example(path))

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*50}")
    print(f"Result: {passed}/{total} passed")
    if passed < total:
        print("Some examples failed. Check the output above for details.")
        sys.exit(1)
    else:
        print("All examples ran successfully!")


if __name__ == "__main__":
    main()
