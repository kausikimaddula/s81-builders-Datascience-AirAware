# Data Schema Contract

Use this document to define data sources, expected formats, and quality standards.

**Last Updated:** TBD  
**Owner:** Data Engineering Team

---

## Raw Data Sources

### Air Quality Data

**Source:** [TBD: e.g., OpenWeatherMap API, Government Environmental Agency]  
**Frequency:** [Daily / 6-hourly]  
**Geographic Coverage:** [Single city: TBD]  
**Historical Availability:** [Minimum 1 year recommended]  

### Raw Schema

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| `date` | DATE | 2024-01-15 | UTC; used as primary key |
| `aqi` | INT | 125 | Air Quality Index (0–500 scale) |
| `pm25` | FLOAT | 45.3 | PM2.5 micrograms per cubic meter |
| `pm10` | FLOAT | 78.2 | PM10 micrograms per cubic meter |
| `no2` | FLOAT | 22.1 | Nitrogen dioxide (ppb) |
| `o3` | FLOAT | 35.5 | Ozone (ppb) |
| `co` | FLOAT | 1.2 | Carbon monoxide (ppm) |
| `location` | VARCHAR(50) | "New Delhi" | City name |
| `latitude` | FLOAT | 28.7041 | Decimal degrees |
| `longitude` | FLOAT | 77.1025 | Decimal degrees |

### Quality Expectations

- **Completeness:** Minimum 80% data available per week (max 20% missing)
- **Freshness:** Latest data ≤2 hours old
- **Range validation:** AQI between 0–500; PM2.5 between 0–500
- **Duplicates:** No duplicate (date, location) pairs

---

## Weather Data

**Source:** [TBD: e.g., OpenWeatherMap, NOAA]  
**Frequency:** [6-hourly or daily aggregates]  
**Alignment:** Joined with air quality on (date, location)

### Raw Schema

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| `date` | DATE | 2024-01-15 | UTC |
| `temp_max` | FLOAT | 28.5 | Celsius |
| `temp_min` | FLOAT | 15.2 | Celsius |
| `humidity` | INT | 65 | Percentage (0–100) |
| `wind_speed` | FLOAT | 12.3 | km/h |
| `wind_direction` | INT | 270 | Degrees (0–360) |
| `precipitation` | FLOAT | 0.0 | mm |
| `visibility` | INT | 10000 | meters |

### Quality Expectations

- **Completeness:** Minimum 90% data available per week
- **Range validation:** Temperature -50 to +60°C; humidity 0–100%; wind speed ≥0

---

## Processed Data (for modeling)

**Location:** `data/processed/`  
**Update Frequency:** Daily  

### Processed Dataset Schema

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `date` | DATE | 2024-01-15 | Index |
| `aqi` | INT | 125 | Target variable (current day) |
| `aqi_lag_1` | INT | 118 | Previous day's AQI |
| `aqi_lag_7` | INT | 110 | AQI from 7 days ago |
| `aqi_rolling_mean_7` | FLOAT | 120.5 | 7-day rolling average |
| `temp_max` | FLOAT | 28.5 | Weather feature |
| `humidity` | INT | 65 | Weather feature |
| `wind_speed` | FLOAT | 12.3 | Weather feature |
| `day_of_week` | INT | 2 | Cyclical: 0–6 (Mon–Sun) |
| `month` | INT | 1 | Cyclical: 1–12 |
| `is_weekend` | INT | 0 | Binary: 0=weekday, 1=weekend |
| `season` | VARCHAR(10) | "winter" | Categorical: winter, spring, summer, fall |
| `aqi_next_day` | INT | 132 | **TARGET**: Forecast for next day |

### Data Quality Checks (Automated)

- [ ] No null values in final dataset
- [ ] No duplicate rows
- [ ] All dates consecutive (no missing days)
- [ ] AQI range 0–500, other features in expected bounds
- [ ] Feature statistics logged (mean, std, min, max)

---

## Validation Procedure

1. **During ingestion:** Validate raw data schema against expectations; log any deviations
2. **During processing:** Check for nulls, duplicates, and range violations
3. **Pre-modeling:** Verify feature statistics and output dataset shape
4. **Post-modeling:** Compare test set feature distributions to training set (detect drift)

---

## Changes and Versioning

| Date | Section | Change | Reason |
|------|---------|--------|--------|
| TBD | - | Initial version | Sprint kickoff |

---

## Appendix: API Integration Example

```python
# Pseudocode for data fetching
import requests
import pandas as pd

def fetch_air_quality(api_key, location, days=365):
    """Fetch historical air quality for location."""
    url = f"https://api.openweathermap.org/data/3.0/airpollution/history"
    params = {
        'q': location,
        'appid': api_key,
        'cnt': days
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    df = pd.DataFrame(data['list'])
    return df
```

