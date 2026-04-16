from __future__ import annotations

import io
import json
from typing import Any

import pandas as pd
from fastapi import HTTPException


def parse_uploaded_file(filename: str, payload: bytes) -> pd.DataFrame:
    lower_name = filename.lower()

    if lower_name.endswith(".csv"):
        return pd.read_csv(io.BytesIO(payload))

    if lower_name.endswith(".json"):
        decoded = json.loads(payload.decode("utf-8"))
        if isinstance(decoded, dict):
            decoded = [decoded]
        if not isinstance(decoded, list):
            raise HTTPException(status_code=400, detail="JSON must contain an object or array")
        return pd.DataFrame(decoded)

    raise HTTPException(status_code=400, detail="Only CSV and JSON files are supported")


def normalize_mapping(payload: dict[str, Any]) -> dict[str, str]:
    normalized = {
        str(key).strip().lower(): str(value).strip().lower()
        for key, value in payload.items()
        if str(key).strip() and str(value).strip()
    }
    return normalized