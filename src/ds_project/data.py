"""Data loading and splitting helpers."""

from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from ds_project.config import RANDOM_STATE, RAW_DATA_DIR


def load_csv(name: str, data_dir: Path = RAW_DATA_DIR, **kwargs) -> pd.DataFrame:
    """Read a CSV file from the given data directory."""
    return pd.read_csv(data_dir / name, **kwargs)


def load_example_dataset() -> pd.DataFrame:
    """Return the iris dataset as a DataFrame with a ``target`` column."""
    return load_iris(as_frame=True).frame


def split(
    df: pd.DataFrame,
    target: str = "target",
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split a DataFrame into stratified train/test features and labels."""
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
