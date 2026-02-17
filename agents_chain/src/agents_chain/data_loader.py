from __future__ import annotations

import pandas as pd
import yaml


def load_tsv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t")


def load_problem_definition(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
