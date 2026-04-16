from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ngo_cleaned.db"
TABLE_NAME = "cleaned_complaints"


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue TEXT,
                category TEXT,
                area TEXT,
                date TEXT,
                source_row INTEGER
            )
            """
        )
        conn.commit()


def save_cleaned_data(df: pd.DataFrame) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        conn.commit()


def load_cleaned_data() -> pd.DataFrame:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        try:
            return pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
        except Exception:
            return pd.DataFrame()


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    return df.fillna("Unknown").to_dict(orient="records")


class PredictRequest(BaseModel):
    issues: list[str] = Field(default_factory=list)


class DuplicateScanRequest(BaseModel):
    threshold: float = Field(default=0.88, ge=0.5, le=0.99)
    max_pairs: int = Field(default=200, ge=1, le=2000)


class ImputeRequest(BaseModel):
    issue: str = Field(default="")
    area: str | None = Field(default=None)
    date: str | None = Field(default=None)
