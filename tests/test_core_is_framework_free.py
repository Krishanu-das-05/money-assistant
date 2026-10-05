import ast
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent.parent / "core"


def _django_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules = [node.module]
        else:
            continue
        found += [
            f"{path.relative_to(CORE_DIR.parent)}:{node.lineno} imports {m}"
            for m in modules
            if m.split(".")[0] == "django"
        ]
    return found


def test_core_never_imports_django():
    py_files = sorted(CORE_DIR.rglob("*.py"))
    assert py_files, f"no Python files found under {CORE_DIR}"

    offenders = [hit for path in py_files for hit in _django_imports(path)]

    assert not offenders, "core/ must stay framework-free:\n" + "\n".join(offenders)
