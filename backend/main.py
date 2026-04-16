from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from cleaning import (
    DEFAULT_CATEGORY_MAPPING,
    calculate_stats,
    clean_dataset,
)
from models import (
    DuplicateScanRequest,
    ImputeRequest,
    PredictRequest,
    dataframe_to_records,
    load_cleaned_data,
    save_cleaned_data,
)
from ml_model import (
    detect_duplicate_candidates,
    fill_missing_values,
    impute_single_record,
    load_artifacts,
    train_and_save_artifacts,
)
from utils import normalize_mapping, parse_uploaded_file

app = FastAPI(title="NGO Data Cleaning & Analytics System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
EXPORT_PATH = BASE_DIR / "data" / "cleaned_export.csv"

state: dict[str, Any] = {
    "raw_df": pd.DataFrame(),
    "cleaned_df": load_cleaned_data(),
    "progress": {"percent": 0, "stage": "idle"},
    "category_mapping": DEFAULT_CATEGORY_MAPPING.copy(),
    "ml_artifacts": None,
}


def _set_progress(percent: int, stage: str) -> None:
    state["progress"] = {"percent": max(0, min(100, percent)), "stage": stage}


@app.on_event("startup")
def startup_event() -> None:
    artifacts = load_artifacts()
    if artifacts is None and not state["cleaned_df"].empty:
        artifacts = train_and_save_artifacts(state["cleaned_df"])

    state["ml_artifacts"] = artifacts
    if artifacts is not None and not state["cleaned_df"].empty:
        enriched = fill_missing_values(state["cleaned_df"], artifacts)
        state["cleaned_df"] = enriched
        save_cleaned_data(enriched)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "NGO Data Cleaning & Analytics API is running"}


@app.post("/upload")
async def upload_data(file: UploadFile = File(...)) -> dict[str, Any]:
    _set_progress(5, "Reading uploaded file")
    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    raw_df = parse_uploaded_file(file.filename or "", payload)
    if raw_df.empty:
        raise HTTPException(status_code=400, detail="No records found in uploaded file")

    state["raw_df"] = raw_df

    cleaned_df = clean_dataset(
        raw_df,
        category_mapping=state["category_mapping"],
        progress_callback=_set_progress,
    )

    artifacts = train_and_save_artifacts(cleaned_df)
    cleaned_df = fill_missing_values(cleaned_df, artifacts)

    state["cleaned_df"] = cleaned_df
    state["ml_artifacts"] = artifacts
    save_cleaned_data(cleaned_df)

    return {
        "message": "Data uploaded and cleaned successfully",
        "raw_rows": int(len(raw_df)),
        "cleaned_rows": int(len(cleaned_df)),
        "preview": dataframe_to_records(raw_df.head(5)),
    }


@app.get("/cleaned-data")
def get_cleaned_data(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    area: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=200),
) -> dict[str, Any]:
    df = state["cleaned_df"].copy()
    if df.empty:
        return {"total": 0, "page": page, "page_size": page_size, "data": []}

    if search:
        needle = search.strip().lower()
        df = df[
            df["issue"].str.lower().str.contains(needle)
            | df["category"].str.lower().str.contains(needle)
            | df["area"].str.lower().str.contains(needle)
        ]

    if category:
        df = df[df["category"].str.lower() == category.strip().lower()]

    if area:
        df = df[df["area"].str.lower() == area.strip().lower()]

    total = int(len(df))
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": dataframe_to_records(df.iloc[start:end]),
    }


@app.get("/stats")
def get_stats() -> dict[str, Any]:
    return calculate_stats(state["cleaned_df"])


@app.get("/download")
def download_cleaned_data() -> FileResponse:
    df = state["cleaned_df"]
    if df.empty:
        raise HTTPException(status_code=404, detail="No cleaned data available")

    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(EXPORT_PATH, index=False)
    return FileResponse(
        path=EXPORT_PATH,
        media_type="text/csv",
        filename="cleaned_ngo_complaints.csv",
    )


@app.get("/progress")
def get_progress() -> dict[str, Any]:
    return state["progress"]


@app.get("/mappings")
def get_mappings() -> dict[str, dict[str, str]]:
    return {"category_mapping": state["category_mapping"]}


@app.put("/mappings")
def update_mappings(payload: dict[str, str]) -> dict[str, Any]:
    if not payload:
        raise HTTPException(status_code=400, detail="Mapping payload cannot be empty")

    normalized = normalize_mapping(payload)
    if not normalized:
        raise HTTPException(status_code=400, detail="No valid mappings found")

    state["category_mapping"] = normalized
    return {"message": "Category mappings updated", "category_mapping": normalized}


@app.post("/duplicates/scan")
def scan_duplicates(payload: DuplicateScanRequest) -> dict[str, Any]:
    df = state["cleaned_df"]
    if df.empty:
        return {"count": 0, "pairs": []}

    pairs = detect_duplicate_candidates(
        df,
        threshold=payload.threshold,
        max_pairs=payload.max_pairs,
    )
    return {"count": len(pairs), "pairs": pairs}


@app.post("/ml/train")
def train_ml_model() -> dict[str, Any]:
    df = state["cleaned_df"]
    if df.empty:
        raise HTTPException(status_code=400, detail="Upload and clean data before training")

    try:
        artifacts = train_and_save_artifacts(df)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state["ml_artifacts"] = artifacts
    return {"message": "ML model trained", **artifacts.get("metadata", {})}


@app.post("/ml/predict")
def predict_with_ml(payload: PredictRequest) -> dict[str, Any]:
    artifacts = state.get("ml_artifacts") or load_artifacts()
    if not artifacts:
        raise HTTPException(status_code=400, detail="Train model first via /ml/train")

    if not payload.issues:
        raise HTTPException(status_code=400, detail="Provide at least one issue text")

    from cleaning import predict_categories

    model = artifacts.get("category_model")
    if model is None:
        raise HTTPException(status_code=400, detail="No category model is available")

    results = predict_categories(model, payload.issues)
    return {
        "model": artifacts.get("metadata", {}),
        "predictions": results,
    }


@app.post("/ml/impute")
def impute_record(payload: ImputeRequest) -> dict[str, Any]:
    artifacts = state.get("ml_artifacts") or load_artifacts()
    if not artifacts:
        raise HTTPException(status_code=400, detail="Train model first via /ml/train")

    result = impute_single_record(payload.model_dump(), artifacts)
    return {
        "model": artifacts.get("metadata", {}),
        "result": result,
    }
