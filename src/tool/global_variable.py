from pathlib import Path
from shutil import rmtree

CWD = Path.cwd()
MAIN = CWD / "src/main"
GENERATED = CWD / "src/generated"

NAMESPACE = "..."

COLORS = [
    "black",
    "blue",
    "brown",
    "cyan",
    "gray",
    "green",
    "light_blue",
    "light_gray",
    "lime",
    "magenta",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
]


def make_dir(path: Path, rmdir: bool = False) -> Path:
    """Create a directory if it does not exist."""
    if rmdir:
        rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
