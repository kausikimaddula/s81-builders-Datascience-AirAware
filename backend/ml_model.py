from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline

from cleaning import _normalize_text

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_PATH = DATA_DIR / "ngo_ml_artifacts.joblib"


def _build_text_classifier(df: pd.DataFrame, target_column: str) -> Pipeline | None:
    train_df = df[["issue", target_column]].copy()
    train_df["issue"] = train_df["issue"].fillna("").astype(str).apply(_normalize_text)
    train_df[target_column] = train_df[target_column].fillna("").astype(str).str.lower()
    train_df = train_df[(train_df["issue"].str.len() > 0) & (train_df[target_column].str.len() > 0)]

    if target_column == "category":
        train_df = train_df[~train_df[target_column].isin(["unknown", "other"])]
    else:
        train_df = train_df[train_df[target_column] != "unknown"]

    if len(train_df) < 4 or train_df[target_column].nunique() < 2:
        return None

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=600, multi_class="auto")),
        ]
    )
    model.fit(train_df["issue"], train_df[target_column])
    return model


def train_and_save_artifacts(df: pd.DataFrame) -> dict[str, Any]:
    previous_artifacts = load_artifacts() or {}

    category_model = _build_text_classifier(df, "category")
    area_model = _build_text_classifier(df, "area")

    if category_model is None:
        category_model = previous_artifacts.get("category_model")

    if area_model is None:
        area_model = previous_artifacts.get("area_model")

    artifacts: dict[str, Any] = {
        "category_model": category_model,
        "area_model": area_model,
        "metadata": {
            "trained_rows": int(len(df)),
            "category_labels": int(df.get("category", pd.Series(dtype=str)).nunique()),
            "area_labels": int(df.get("area", pd.Series(dtype=str)).nunique()),
        },
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifacts, MODEL_PATH)
    return artifacts


def load_artifacts() -> dict[str, Any] | None:
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def detect_duplicate_candidates(
    df: pd.DataFrame,
    threshold: float = 0.85,
    max_pairs: int = 200,
) -> list[dict[str, Any]]:
    if df.empty:
        return []

    scoped = df.copy()
    scoped["issue"] = scoped["issue"].fillna("").astype(str).apply(_normalize_text)
    scoped["area"] = scoped["area"].fillna("Unknown").astype(str)
    scoped["date"] = scoped["date"].fillna("").astype(str)

    pairs: list[dict[str, Any]] = []
    for (area, date), group in scoped.groupby(["area", "date"], dropna=False):
        issues = group["issue"].tolist()
        if len(issues) < 2:
            continue

        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(issues)
        similarity_matrix = cosine_similarity(matrix)
        indices = list(group.index)

        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                score = float(similarity_matrix[i, j])
                if score >= threshold:
                    row_a = group.loc[indices[i]]
                    row_b = group.loc[indices[j]]
                    pairs.append(
                        {
                            "index_a": int(indices[i]),
                            "index_b": int(indices[j]),
                            "issue_a": row_a.get("issue", ""),
                            "issue_b": row_b.get("issue", ""),
                            "area": area,
                            "date": date,
                            "similarity": round(score, 4),
                        }
                    )
                    if len(pairs) >= max_pairs:
                        return pairs

    return pairs


def _predict_with_model(model: Any | None, values: list[str]) -> list[str]:
    if model is None or not values:
        return []
    cleaned_values = [_normalize_text(value) for value in values]
    cleaned_values = [value if value else "unknown" for value in cleaned_values]
    return [str(item) for item in model.predict(cleaned_values)]


def _predict_top_label(model: Any | None, value: str) -> tuple[str, float]:
    cleaned_value = _normalize_text(value) or "unknown"
    if model is None:
        return "other", 0.0

    predicted = str(model.predict([cleaned_value])[0])
    confidence = 1.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([cleaned_value])[0]
        confidence = float(np.max(probabilities))
    return predicted, confidence


def fill_missing_values(df: pd.DataFrame, artifacts: dict[str, Any] | None) -> pd.DataFrame:
    if df.empty:
        return df

    enriched = df.copy()
    artifacts = artifacts or {}
    category_model = artifacts.get("category_model")
    area_model = artifacts.get("area_model")

    category_predictions = _predict_with_model(
        category_model,
        enriched["issue"].fillna("").astype(str).tolist(),
    )
    area_predictions = _predict_with_model(
        area_model,
        enriched["issue"].fillna("").astype(str).tolist(),
    )

    for idx in range(len(enriched)):
        current_category = str(enriched.at[idx, "category"]) if "category" in enriched else ""
        current_area = str(enriched.at[idx, "area"]) if "area" in enriched else ""

        if current_category in {"", "unknown", "other", "nan"} and idx < len(category_predictions):
            enriched.at[idx, "category"] = category_predictions[idx]

        if current_area in {"", "unknown", "nan"} and idx < len(area_predictions):
            enriched.at[idx, "area"] = area_predictions[idx].title()

    return enriched


def impute_single_record(record: dict[str, Any], artifacts: dict[str, Any] | None) -> dict[str, Any]:
    issue_text = _normalize_text(record.get("issue", ""))
    provided_area = str(record.get("area", "") or "").strip()
    provided_date = str(record.get("date", "") or "").strip()

    category_model = (artifacts or {}).get("category_model")
    area_model = (artifacts or {}).get("area_model")

    predicted_category, category_confidence = _predict_top_label(category_model, issue_text)
    predicted_area, area_confidence = _predict_top_label(area_model, issue_text)

    if provided_area:
        normalized_area = provided_area.title()
    else:
        normalized_area = predicted_area.title() if predicted_area else "Predicted Area"

    try:
        parsed_date = pd.to_datetime(provided_date, errors="coerce", dayfirst=True)
        normalized_date = parsed_date.strftime("%Y-%m-%d") if not pd.isna(parsed_date) else ""
    except Exception:
        normalized_date = ""

    return {
        "issue": issue_text,
        "category": predicted_category,
        "category_confidence": round(category_confidence, 4),
        "area": normalized_area or "Predicted Area",
        "area_confidence": round(area_confidence, 4),
        "date": normalized_date,
    }