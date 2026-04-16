# NGO Data Cleaning & Analytics System

A full-stack application to upload NGO complaint data, run a structured data-cleaning pipeline, and visualize key insights.

## Tech Stack

- Frontend: React + Tailwind CSS + Axios + Recharts
- Backend: FastAPI + Pandas + NumPy
- Persistence: SQLite (for cleaned dataset snapshots)

## Project Structure

```text
/backend
  main.py
  cleaning.py
  models.py
  requirements.txt
/frontend
  src/components
  src/pages
  src/services
```

## Backend Setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://127.0.0.1:5173 and backend on http://127.0.0.1:8001.

## API Endpoints

- POST /upload: Upload CSV or JSON and trigger cleaning pipeline
- GET /cleaned-data: Fetch cleaned records with search/filter/pagination
- GET /stats: Fetch analytics for charts
- GET /download: Download cleaned CSV
- GET /progress: Check cleaning progress
- GET /mappings: Get category mappings
- PUT /mappings: Update category mappings
- POST /duplicates/scan: Find probable duplicate complaint pairs
- POST /ml/train: Train text classifier from cleaned data
- POST /ml/predict: Predict category for issue text

## Data Cleaning Rules

1. Exact duplicate removal and fuzzy duplicate detection
2. Missing critical fields dropped (`issue`, `date`)
3. Text and date normalization
4. Area standardization and category label normalization
5. Special character cleanup and whitespace normalization
6. Validation for future dates and empty required fields

## Optional ML Extensions

This project now includes scikit-learn based auto-categorization endpoints.

## Run Notes

- Backend is a FastAPI app, so run `uvicorn main:app --reload --port 8001` inside backend.
- Frontend is a Vite app, so run `npm run dev` inside frontend.
- `npm start` is not used for this setup.
