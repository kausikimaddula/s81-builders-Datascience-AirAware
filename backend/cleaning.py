from __future__ import annotations

import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any, Callable

import numpy as np
import pandas as pd

DEFAULT_CATEGORY_MAPPING = {
    "water issue": "water",
    "water": "water",
    "h2o problem": "water",
    "electricity": "electricity",
    "power cut": "electricity",
    "drainage": "sanitation",
    "garbage": "sanitation",
    "medical": "health",
}

AREA_MAPPING = {
    "hyd": "Hyderabad",
    "hyderabad": "Hyderabad",
    "secunderabad": "Secunderabad",
    "vizag": "Visakhapatnam",
    "vskp": "Visakhapatnam",
    "blr": "Bengaluru",
    "bangalore": "Bengaluru",
    "chennai": "Chennai",
    "chenni": "Chennai",
    "chen": "Chennai",
}

REQUIRED_COLUMNS = ["issue", "date"]
OPTIONAL_COLUMNS = ["area", "category"]


def _normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _normalize_area(value: object) -> str:
    normalized = _normalize_text(value)
    if not normalized:
        return "Unknown"
    return AREA_MAPPING.get(normalized, normalized.title())


def _category_from_issue(issue: str, mapping: dict[str, str]) -> str:
    if not issue:
        return "unknown"

    if issue in mapping:
        return mapping[issue]

    for key, category in mapping.items():
        if key in issue or issue in key:
            return category

    return "other"


def _drop_fuzzy_duplicates(df: pd.DataFrame, threshold: float = 0.92) -> pd.DataFrame:
    if df.empty:
        return df

    deduped_rows: list[int] = []
    accepted: list[tuple[str, str, str]] = []

    for idx, row in df.iterrows():
        issue = row.get("issue", "")
        area = row.get("area", "Unknown")
        date = row.get("date", "")

        is_duplicate = False
        for kept_issue, kept_area, kept_date in accepted:
            if area == kept_area and date == kept_date:
                similarity = SequenceMatcher(None, issue, kept_issue).ratio()
                if similarity >= threshold:
                    is_duplicate = True
                    break

        if not is_duplicate:
            deduped_rows.append(idx)
            accepted.append((issue, area, date))

    return df.loc[deduped_rows].reset_index(drop=True)


def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [_normalize_text(col) for col in cleaned.columns]

    for col in REQUIRED_COLUMNS + OPTIONAL_COLUMNS:
        if col not in cleaned.columns:
            cleaned[col] = np.nan

    return cleaned


def clean_dataset(
    raw_df: pd.DataFrame,
    category_mapping: dict[str, str] | None = None,
    progress_callback: Callable[[int, str], None] | None = None,
) -> pd.DataFrame:
    mapping = {
        _normalize_text(k): _normalize_text(v)
        for k, v in (category_mapping or DEFAULT_CATEGORY_MAPPING).items()
    }

    def update_progress(percent: int, stage: str) -> None:
        if progress_callback:
            progress_callback(percent, stage)

    update_progress(10, "Preparing dataframe")
    df = _ensure_columns(raw_df)

    update_progress(25, "Normalizing text fields")
    df["issue"] = df["issue"].apply(_normalize_text)
    df["area"] = df["area"].apply(_normalize_area)

    update_progress(40, "Standardizing dates")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["issue", "date"])

    # Reject empty issue text and future dates.
    now_utc = datetime.now(timezone.utc).date()
    df = df[df["issue"].str.len() > 0]
    df = df[df["date"].dt.date <= now_utc]

    update_progress(55, "Applying category mappings")
    df["category"] = df["issue"].apply(lambda issue: _category_from_issue(issue, mapping))

    update_progress(70, "Handling missing values")
    for col in OPTIONAL_COLUMNS:
        df[col] = df[col].fillna("Unknown")

    update_progress(80, "Removing duplicates")
    df = df.drop_duplicates(subset=["issue", "area", "date"])
    df = _drop_fuzzy_duplicates(df)

    update_progress(92, "Formatting output")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df = df.reset_index(drop=True)
    df["source_row"] = df.index + 1

    update_progress(100, "Completed")
    return df


def calculate_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_complaints": 0,
            "category_counts": [],
            "area_distribution": [],
            "time_trends": [],
        }

    category_counts = (
        df.groupby("category").size().sort_values(ascending=False).reset_index(name="count")
    )
    area_distribution = (
        df.groupby("area").size().sort_values(ascending=False).reset_index(name="count")
    )
    time_trends = df.groupby("date").size().reset_index(name="count").sort_values("date")

    return {
        "total_complaints": int(len(df)),
        "category_counts": category_counts.to_dict(orient="records"),
        "area_distribution": area_distribution.to_dict(orient="records"),
        "time_trends": time_trends.to_dict(orient="records"),
    }


def detect_potential_duplicates(
    df: pd.DataFrame,
    threshold: float = 0.88,
    max_pairs: int = 200,
) -> list[dict[str, Any]]:
    if df.empty:
        return []

    scoped = df.copy()
    scoped["issue"] = scoped["issue"].fillna("").astype(str)
    scoped["area"] = scoped["area"].fillna("Unknown").astype(str)
    scoped["date"] = scoped["date"].fillna("").astype(str)

    pairs: list[dict[str, Any]] = []
    grouped = scoped.groupby(["area", "date"], dropna=False)

    for (area, date), group in grouped:
        records = list(group.iterrows())
        for i in range(len(records)):
            idx_a, row_a = records[i]
            issue_a = _normalize_text(row_a.get("issue", ""))
            if not issue_a:
                continue

            for j in range(i + 1, len(records)):
                idx_b, row_b = records[j]
                issue_b = _normalize_text(row_b.get("issue", ""))
                if not issue_b:
                    continue

                similarity = SequenceMatcher(None, issue_a, issue_b).ratio()
                if similarity >= threshold:
                    pairs.append(
                        {
                            "index_a": int(idx_a),
                            "index_b": int(idx_b),
                            "issue_a": row_a.get("issue", ""),
                            "issue_b": row_b.get("issue", ""),
                            "area": area,
                            "date": date,
                            "similarity": round(float(similarity), 4),
                        }
                    )
                    if len(pairs) >= max_pairs:
                        return pairs

    return pairs


def train_issue_classifier(df: pd.DataFrame) -> tuple[Any, dict[str, Any]]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
    except ImportError as exc:
        raise RuntimeError("scikit-learn is required for ML endpoints") from exc

    if df.empty:
        raise ValueError("No cleaned data available for training")

    train_df = df[["issue", "category"]].copy()
    train_df["issue"] = train_df["issue"].fillna("").astype(str).apply(_normalize_text)
    train_df["category"] = train_df["category"].fillna("").astype(str).str.lower()
    train_df = train_df[(train_df["issue"].str.len() > 0) & (train_df["category"].str.len() > 0)]
    train_df = train_df[~train_df["category"].isin(["unknown", "other"])]

    if len(train_df) < 4:
        raise ValueError("Need at least 4 labeled rows to train classifier")

    unique_categories = train_df["category"].nunique()
    if unique_categories < 2:
        raise ValueError("Need at least 2 unique categories to train classifier")

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=600, multi_class="auto")),
        ]
    )
    model.fit(train_df["issue"], train_df["category"])

    metadata = {
        "trained_rows": int(len(train_df)),
        "unique_categories": int(unique_categories),
    }
    return model, metadata


def predict_categories(model: Any, issues: list[str]) -> list[dict[str, Any]]:
    cleaned_issues = [_normalize_text(issue) for issue in issues]
    predictions = model.predict(cleaned_issues)

    confidences: list[float]
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(cleaned_issues)
        confidences = [float(np.max(row)) for row in probs]
    else:
        confidences = [1.0 for _ in cleaned_issues]

    return [
        {
            "issue": original,
            "normalized_issue": normalized,
            "predicted_category": str(prediction),
            "confidence": round(confidence, 4),
        }
        for original, normalized, prediction, confidence in zip(
            issues, cleaned_issues, predictions, confidences
        )
    ]
