# RUNBOOK: AirAware Setup & Execution Guide

**Project:** AirAware  
**Last Updated:** TBD  
**Audience:** New developers, contributors, and deployment engineers  

This guide enables a new team member to set up the project, fetch data, train the model, and deploy the dashboard in <1 hour.

---

## Prerequisites

- **OS:** Linux, macOS, or Windows (with WSL)
- **Python:** 3.9 or later
- **Git:** Installed and configured
- **API Keys:** OpenWeatherMap API key (free tier available)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/AirAware.git
cd AirAware
git checkout main
```

---

## 2. Set Up Python Environment

### Option A: Using venv (Recommended for Simplicity)

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using conda

```bash
conda env create -f environment.yml
conda activate airaware
```

---

## 3. Configure API Keys

Create a `.env` file in the project root (this file is git-ignored):

```
OPENWEATHER_API_KEY=your_api_key_here
TARGET_CITY=New Delhi
TARGET_LAT=28.7041
TARGET_LON=77.1025
```

**Get API Key:** Sign up at https://openweathermap.org/api (free tier available)

---

## 4. Fetch Data

### Download Historical Data (One-Time)

```bash
python src/fetch_data.py --mode historical --days 365
```

**Output:** `data/raw/historical_aqi_weather.csv`

### Fetch Today's Data (Daily)

```bash
python src/fetch_data.py --mode daily
```

---

## 5. Prepare Data for Modeling

```bash
python src/prepare_data.py
```

**Input:** `data/raw/historical_aqi_weather.csv`  
**Output:** `data/processed/features_for_modeling.csv`

**Sanity Checks:**
- No null values
- Feature ranges match expectations
- 365 ± 5 rows (accounting for missing days)

---

## 6. Train the Model

```bash
python src/train_model.py --model random_forest --output-dir models/
```

**Input:** `data/processed/features_for_modeling.csv`  
**Output:** 
- `models/aqi_forecast_v1.0.pkl` (trained model)
- `outputs/model_metrics.json` (performance results)

**Expected Performance:**
- MAE: <20 AQI points
- R²: >0.70 on test set

---

## 7. Generate Predictions

### Batch Prediction (for historical validation)

```bash
python src/generate_predictions.py --input data/processed/features_for_modeling.csv \
  --model models/aqi_forecast_v1.0.pkl --output outputs/predictions.csv
```

### Single Prediction (for app inference)

```python
from src.inference import predict_next_day_aqi
forecast = predict_next_day_aqi(
    last_aqi=145,
    temp_max=28.5,
    humidity=65,
    wind_speed=12.3
)
print(forecast)  # Output: {"aqi_forecast": 148, "confidence": "±15"}
```

---

## 8. Run the Web Dashboard

### Start the Backend API

```bash
python app/app.py --port 5000
```

**Output:** `Running on http://localhost:5000`

### Start the Frontend (if separate)

```bash
cd app/frontend
npm install
npm start
```

**Output:** `http://localhost:3000`

---

## 9. Validate Deployment

### Test API Endpoints

```bash
# Get current AQI
curl http://localhost:5000/api/current

# Get forecast
curl http://localhost:5000/api/forecast

# Health check
curl http://localhost:5000/health
```

### Expected Responses

```json
{
  "aqi": 145,
  "status": "Moderate",
  "recommendation": "Sensitive groups should limit outdoor activities",
  "timestamp": "2024-01-16T10:30:00Z"
}
```

---

## 10. Deploy to Production

### Using Heroku (Fastest for MVP)

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create airaware-app

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Live URL:** `https://airaware-app.herokuapp.com`

### Using DigitalOcean (More Control)

1. Create a Droplet (Ubuntu 20.04, basic plan)
2. SSH into droplet:
   ```bash
   ssh root@your_droplet_ip
   ```
3. Clone repo and repeat steps 1–6
4. Use `gunicorn` to run app:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:80 app.app:app
   ```
5. Set up domain and SSL (Nginx + Let's Encrypt)

---

## 11. Monitor & Update Data

### Automatic Daily Refresh (Optional)

Set up a cron job to update data every day at 12:00 UTC:

```bash
# Edit crontab
crontab -e

# Add this line
0 12 * * * /path/to/venv/bin/python /path/to/AirAware/src/fetch_data.py --mode daily
```

### Manual Refresh

```bash
python src/fetch_data.py --mode daily && python src/prepare_data.py
```

---

## 12. Troubleshooting

### Issue: "API key invalid"

**Solution:** Verify `.env` file exists and API key is correct. Test with:
```bash
curl "https://api.openweathermap.org/data/3.0/airpollution/history?q=New%20Delhi&appid=YOUR_KEY"
```

### Issue: "Model file not found"

**Solution:** Ensure you ran `python src/train_model.py` before starting the app.

### Issue: "Port 5000 already in use"

**Solution:** Use a different port:
```bash
python app/app.py --port 8080
```

Or kill the process using the port:
```bash
# macOS/Linux
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Issue: "Data file is stale (>2 days old)"

**Solution:** Manually refetch:
```bash
python src/fetch_data.py --mode daily
```

---

## 13. Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Integration Test (End-to-End)

```bash
python tests/integration_test.py
```

**Expected:** All API endpoints return 200; predictions are in range 0–500

---

## 14. Documentation

Refer to these docs for deeper context:

- **Project Plan:** [PROJECT_PLAN.md](../PROJECT_PLAN.md)
- **Data Schema:** [DATA_SCHEMA.md](DATA_SCHEMA.md)
- **Model Card:** [MODEL_CARD.md](MODEL_CARD.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) (TBD)

---

## 15. Common Tasks

### Add a New Feature to the Model

1. Edit `src/feature_engineering.py`
2. Rerun: `python src/prepare_data.py`
3. Retrain: `python src/train_model.py`
4. Compare metrics in `outputs/model_metrics.json`

### Change Target City

1. Update `.env`:
   ```
   TARGET_CITY=Mumbai
   TARGET_LAT=19.0760
   TARGET_LON=72.8777
   ```
2. Refetch data: `python src/fetch_data.py --mode historical --days 365`
3. Retrain model

### Deploy Model Update

1. Train model locally
2. Commit `models/aqi_forecast_v*.pkl`
3. Push to GitHub
4. Heroku auto-deploys on `push to main`

---

## 16. Support & Questions

- **GitHub Issues:** Report bugs at https://github.com/your-org/AirAware/issues
- **Team Slack:** #airaware-dev
- **Weekly Standup:** Friday 10:00 AM UTC

---

**Last Verified:** TBD  
**Verified By:** [Name]  
**Status:** ✓ Working / ⚠ Needs update
