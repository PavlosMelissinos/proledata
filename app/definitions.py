from pathlib import Path


def project_root() -> Path:
    """Return project root folder."""
    return Path(__file__).parent.parent
