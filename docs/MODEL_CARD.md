# Model Card — AirAware Next-Day AQI Forecast

**Model Name:** AirAware AQI Forecaster  
**Version:** 1.0  
**Date:** TBD  
**Owner:** ML Engineering Team  

Use this template to document your trained model. Complete during Week 3 of the sprint.

---

## Model Details

### Model Architecture

- **Type:** [e.g., Linear Regression, Random Forest, Gradient Boosting]
- **Framework:** [scikit-learn, XGBoost, etc.]
- **Task:** Regression (next-day AQI forecast)
- **Target Variable:** `aqi_next_day` (continuous, range 0–500)

### Input Features

| Feature | Type | Description |
|---------|------|-------------|
| `aqi_lag_1` | numeric | Previous day's AQI |
| `aqi_lag_7` | numeric | AQI from 7 days ago |
| `aqi_rolling_mean_7` | numeric | 7-day rolling average |
| `temp_max` | numeric | Maximum temperature |
| `humidity` | numeric | Relative humidity |
| `wind_speed` | numeric | Wind speed |
| `day_of_week` | categorical | Encoded as one-hot |
| `season` | categorical | Encoded as one-hot |

### Training Data

- **Time Period:** [e.g., 2023-01-01 to 2023-12-31]
- **Sample Size:** [e.g., 365 days; adjust for missing data]
- **Geographic Location:** [e.g., New Delhi, India]
- **Data Quality:** [e.g., 85% completeness; gaps filled via forward-fill]

---

## Model Performance

### Validation Strategy

- **Test Period:** Last 60 days (held out; not used in training)
- **Cross-Validation:** Time-series 5-fold (to prevent data leakage)
- **Baseline:** Simple persistence forecast (tomorrow = today AQI); MAE = [TBD]

### Performance Metrics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| **MAE** | [TBD] | <20 AQI | ✓ Pass / ✗ Fail |
| **RMSE** | [TBD] | <30 AQI | ✓ Pass / ✗ Fail |
| **R² (test)** | [TBD] | >0.70 | ✓ Pass / ✗ Fail |
| **MAPE** | [TBD]% | <15% | ✓ Pass / ✗ Fail |

### Performance by Season

| Season | MAE | RMSE | Notes |
|--------|-----|------|-------|
| Winter | [TBD] | [TBD] | [e.g., High error; few samples] |
| Spring | [TBD] | [TBD] | |
| Summer | [TBD] | [TBD] | |
| Fall | [TBD] | [TBD] | |

---

## Limitations & Biases

### Known Limitations

- **Forecast Horizon:** Only 1-day ahead; multi-day forecasts degrade quickly
- **Geography:** Trained on single city; generalization to other cities unknown
- **Data Gaps:** Model trained on data with [TBD]% missing values; may be biased toward periods with dense measurements
- **Extreme Events:** Performance on very high AQI days (>300) not separately validated

### Potential Biases

- **Seasonal Bias:** [e.g., Model underestimates AQI during winter monsoons; reason = few training samples]
- **Day-of-Week Effect:** [e.g., Lower AQI predicted on weekends due to reduced traffic; may not generalize across years]

### Scenarios Not Covered

- Major pollution events (e.g., fireworks, industrial accidents)
- Structural changes (e.g., new factories, traffic policies)
- Climate anomalies (e.g., unusual weather patterns)

---

## Deployment & Inference

### Model Artifact

- **File Location:** `models/aqi_forecast_v1.0.pkl`
- **Size:** [e.g., 2.3 MB]
- **Dependencies:** scikit-learn==1.3.0, pandas==2.0.0
- **Load Example:**
  ```python
  import pickle
  model = pickle.load(open('models/aqi_forecast_v1.0.pkl', 'rb'))
  prediction = model.predict([[aqi_lag_1, aqi_lag_7, temp_max, ...]])
  ```

### Inference Pipeline

1. Load raw data (today's air quality + weather forecast)
2. Apply feature transformations (rolling means, cyclical encoding)
3. Generate prediction using model
4. Output: `aqi_forecast`, `confidence_interval` (e.g., ±15 AQI points)

### API Signature

```
POST /api/forecast
Input: {
  "location": "New Delhi",
  "date": "2024-01-16"
}
Output: {
  "aqi_forecast": 145,
  "confidence_lower": 130,
  "confidence_upper": 160,
  "recommendation": "Moderate; sensitive groups should limit outdoor activities"
}
```

---

## Model Maintenance

### Retraining Schedule

- **Frequency:** Monthly (first day of month) or upon request
- **Trigger:** If test-set MAE increases >25% from baseline

### Monitoring Metrics

Track these metrics in production:
- Distribution of predictions vs. actuals
- Forecast error by day-of-week, season
- Data missingness in ingestion pipeline

### Refresh Requirements

| Refresh Interval | Data Sources | Trigger |
|------------------|--------------|---------|
| Daily | Today's air quality + weather | Automatic at 12:00 UTC |
| Monthly | Retrain on updated dataset | First day of month |
| Quarterly | Validate test performance | Business review |

---

## Ethical Considerations

### Intended Use

- **Primary:** Help users make informed decisions about outdoor activity based on air quality
- **Not intended for:** Medical diagnosis, clinical decision-making, regulatory compliance

### Potential Harms & Mitigations

| Risk | Mitigation |
|------|-----------|
| Users over-rely on forecast and ignore health risks | Display uncertainty range; recommend consulting health professionals |
| Model bias systematically underpredicts for certain populations | Monitor disparities across neighborhoods; adjust with additional data |
| Forecast failure during critical periods | Include uptime guarantee; provide fallback guidance |

---

## References & Documentation

- AQI Standards: https://www.airnow.gov/aqi/aqi-basics/
- Feature Engineering Log: `notebooks/02_feature_engineering.ipynb`
- Model Training Code: `src/train_model.py`
- Hyperparameter Tuning Results: `outputs/hyperparams_log.csv`

---

## Approval & Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| ML Engineer | [TBD] | [TBD] | Draft / ✓ Approved |
| Data Engineer | [TBD] | [TBD] | ✓ Approved |
| Project Manager | [TBD] | [TBD] | ✓ Approved |

