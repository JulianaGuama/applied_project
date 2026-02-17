"""I/O helpers for loading YAML configuration and datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import DatasetSnapshot


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return a dictionary."""

    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_dataset(path: str | Path) -> DatasetSnapshot:
    """Load dataset YAML and parse as DatasetSnapshot."""

    payload = load_yaml_file(path)
    return DatasetSnapshot(**payload)
