# AirAware: 4-Week Data Science Project Plan

**Project:** AirAware  
**Duration:** 4 weeks (28 days)  
**Last Updated:** April 1, 2026  

---

## 1. Problem Statement & Solution Overview

### Real-World Problem

Air pollution in urban areas poses documented health risks. Citizens often lack real-time, accessible information about local air quality trends and whether current or forecast conditions warrant behavior changes (e.g., reducing outdoor time, using protective equipment).

### Who It Affects

- **Primary Users:** Citizens in a target city (age 18-65, with internet access, concerned about air quality)
- **Secondary Users:** Vulnerable populations (children, elderly, individuals with respiratory conditions) who depend on caregivers for information

### How Data & ML Contribute

1. **Data gathering:** Integrate air quality measurements (AQI, PM2.5, PM10) and weather data from public APIs
2. **Analysis:** Identify pollution patterns, seasonal trends, and correlations with weather conditions
3. **Forecasting:** Build a model to predict next-day air quality, enabling users to plan activities
4. **Communication:** Deliver risk levels and actionable guidance through a simple web interface

### User Interaction Model

Users will access a web dashboard where they can:
- View **today's air quality** (real measurement + risk classification)
- See **historical trends** (last 7 days, last 30 days)
- View **next-day forecast** (predicted AQI category and confidence)
- Receive a **risk-based recommendation** (e.g., "Good day for outdoor activity" vs. "Limit outdoor exposure")

### Why This Approach Avoids Complexity

- No mobile app; dashboard is browser-based
- Forecast horizon is 1 day (not weeks or months)
- Single city MVP to avoid data aggregation overhead
- Pre-defined risk categories (not custom thresholds per user)

---

## 2. Dataset Selection & Scope

### Chosen Datasets

#### Primary: Air Quality Data
- **Source:** OpenWeatherMap API (or local government environmental agency)
- **Variables:** AQI, PM2.5, PM10, NO2, O3, CO (daily averages)
- **Frequency:** Daily measurements
- **Historical coverage:** Minimum 1 year (365 days) for seasonal patterns
- **Scope:** Single location (latitude/longitude) for MVP

#### Secondary: Weather Data
- **Source:** OpenWeatherMap API
- **Variables:** Temperature, humidity, wind speed, wind direction, precipitation
- **Frequency:** Daily or 6-hourly aggregates
- **Purpose:** Feature engineering for forecasting model

### Scope Decisions

| Aspect | In Scope | Out of Scope |
|--------|----------|--------------|
| Geographic | Single city (e.g., Delhi, San Francisco, London) | Multi-city aggregation, regional analysis |
| Time horizon | Historical + 1-day forecast | Long-term forecasts (>7 days) |
| Pollutants | Major indicators (PM2.5, AQI) | Individual chemical analysis |
| Users | General population | Real-time alerts to specific apps or SMS |
| Data quality | Handle missing values, interpolation | Advanced anomaly detection, data correction |

### Quality Checks

- **Availability:** Confirm API access and rate limits before sprint start
- **Completeness:** Minimum 80% data availability; flag periods with >20% gaps
- **Relevance:** Verify that chosen city has consistent, reliable measurements

### What Is Explicitly Out of Scope

- Real-time data ingestion (batch daily ingestion acceptable)
- Multi-year forecasting model
- Custom health risk mapping per user profile
- Mobile app or push notifications

---

## 3. Roles & Responsibilities

### Team Composition (Recommended: 2–3 people)

| Role | Responsibilities | Required Skills |
|------|------------------|-----------------|
| **Data Engineer** | Data ingestion, cleaning, storage | Python, APIs, pandas, SQL basics |
| **ML Engineer** | EDA, feature engineering, model training, evaluation | Python, scikit-learn, statistical analysis |
| **App Developer** | Web dashboard, frontend deployment, integration testing | Flask/FastAPI, HTML/CSS, deployment (e.g., Heroku) |

### Collaboration Points

- **Week 1 kickoff:** Define target city, confirm data sources, review project plan
- **End of Week 2:** Data and features ready for modeling; app skeleton deployed
- **End of Week 3:** Model trained and tested; app integrated with predictions
- **Week 4:** End-to-end testing, documentation, full deployment

### Knowledge Sharing

- Weekly standups (15 min): blockers, progress, help needed
- Shared documentation in `/docs/` for contracts and decisions
- Code reviews on all PRs before merge to main

---

## 4. Sprint Timeline (4 Weeks)

### Week 1: Foundation & Data Acquisition

**Goal:** Confirm data sources, set up environment, begin ingestion

| Day | Task | Owner | Deliverable |
|-----|------|-------|------------|
| Mon–Tue | Environment setup (Python venv, requirements.txt, git workflow) | Team | Working local and shared environments |
| Wed–Thu | Confirm data APIs, test connections, document schemas | Data Eng | Data ingestion script (draft) |
| Fri | EDA on raw data; identify gaps and quality issues | ML Eng | Jupyter notebook with initial findings |

**End-of-Week Checkpoint:** 
- Environments working
- Data accessible and validated
- Initial EDA complete; quality report filed

---

### Week 2: Data Preparation & Model Setup

**Goal:** Clean and transform data; establish baseline; deploy app scaffold

| Day | Task | Owner | Deliverable |
|-----|------|-------|------------|
| Mon–Tue | Data cleaning, missing value handling, merge air quality + weather | Data Eng | Processed dataset in `data/processed/` |
| Wed | Feature engineering (lag features, rolling means, cyclical encoding for day-of-week) | ML Eng | Feature transformation pipeline in `src/` |
| Thu | Baseline model training (simple linear regression or decision tree) | ML Eng | Trained model artifact + metrics report |
| Fri | App scaffold deployed (Flask/FastAPI with dummy predictions) | App Dev | Live URL with static dashboard |

**End-of-Week Checkpoint:**
- Clean data ready for modeling
- Baseline model performance documented
- App deployed and accessible (not yet integrated with real model)

---

### Week 3: Model Refinement & Integration

**Goal:** Improve model, integrate with app, prepare for testing

| Day | Task | Owner | Deliverable |
|-----|------|-------|------------|
| Mon–Tue | Model iteration (hyperparameter tuning, cross-validation, feature selection) | ML Eng | Final model + performance comparison |
| Wed | Create model API endpoint; integrate with app | App Dev + ML Eng | Model predictions served via REST API |
| Thu | End-to-end integration test; verify data→model→UI flow | Team | Integration test report |
| Fri | Document model assumptions, limitations, and data contracts | ML Eng | Model card in `/docs/` |

**End-of-Week Checkpoint:**
- Model integrated into live app
- End-to-end pipeline tested
- Model performance and assumptions documented

---

### Week 4: Testing, Documentation & Deployment

**Goal:** Finalize, test thoroughly, deploy to production, document everything

| Day | Task | Owner | Deliverable |
|-----|------|-------|------------|
| Mon | User acceptance testing (UAT) on dashboard + predictions | Team | UAT checklist completed |
| Tue | Performance testing (app load time, model inference latency) | App Dev | Performance report |
| Wed | Write reproducibility guide (how to run, environment, data refresh) | Data Eng | `RUNBOOK.md` in repo |
| Thu | Final bug fixes, documentation polish, video walkthrough | Team | Bug-free, documented system |
| Fri | Deploy to production; prepare for handoff | App Dev | Live product URL + deployment checklist |

**End-of-Week Checkpoint:**
- Fully tested, documented, and deployed system
- All team members can reproduce the setup
- Live product accessible to users

---

## 5. Deployment & Testing Plan

### Validation Strategy

#### Unit Tests (Week 2–3)
- Data loading and transformation functions
- Feature engineering logic
- Model scoring function

```python
# Example: test/test_data.py
def test_missing_value_handling():
    raw = pd.DataFrame({'aqi': [100, None, 150]})
    cleaned = fill_missing_values(raw)
    assert cleaned['aqi'].isnull().sum() == 0
```

#### Integration Tests (Week 3)
- Data pipeline: ingestion → cleaning → features
- Model API: input data → prediction output
- Dashboard: data retrieval → display

#### User Acceptance Testing (Week 4)
- Dashboard displays correct data for today
- Forecast appears sensible given historical patterns
- No crashes when data is missing or unexpected

### Handling Unexpected Input

- **Missing data:** Daily batch process with fallback to previous day's values
- **Data spikes:** Outlier detection flags suspicious measurements; manual review queued
- **Forecast failure:** Display "Insufficient data for forecast today" rather than crashing
- **API downtime:** Cache last successful fetch; notify user of data staleness

### Deployment Steps

1. Push to `main` branch after code review
2. Automated tests run (GitHub Actions or similar)
3. Docker image built and pushed to registry
4. Deploy to production server (e.g., Heroku, AWS, DigitalOcean)
5. Monitor logs and uptime dashboard

### Rollback Plan

- Keep previous model artifact and code tag available
- If new model performance degrades >5% on validation set, revert and investigate

---

## 6. MVP (Minimum Viable Product)

### Core MVP Features

An MVP is the **smallest subset** that delivers genuine end-to-end value. Everything here is **mandatory** for the project to be considered complete:

1. **Data Pipeline**
   - Daily automated fetch of air quality and weather data
   - Cleaning and feature engineering
   - Storage in local database or CSV

2. **Forecasting Model**
   - Single-day-ahead AQI or PM2.5 forecast
   - Baseline accuracy ≥ mean absolute error of 20 AQI points
   - Confidence interval or uncertainty quantification

3. **Web Dashboard**
   - Display today's air quality (measured)
   - Display next-day forecast (predicted)
   - Simple risk classification (e.g., "Good", "Moderate", "Unhealthy")
   - Historical sparkline (last 30 days)

4. **Reproducibility**
   - Clear setup instructions
   - Requirements.txt or environment.yml
   - Runnable end-to-end pipeline

### What Is NOT MVP

- Mobile app
- Multi-city forecasting
- User accounts or personalization
- Real-time alerts or notifications
- Advanced analytics (e.g., impact attribution, temporal decomposition)

### MVP Success Criteria

- Dashboard loads in <2 seconds
- Forecast updates automatically once daily
- No crashes when data is missing for 1–2 days
- README and RUNBOOK allow new user to set up and run in <1 hour

---

## 7. Functional Requirements

### FR1: Data Ingestion
- **Requirement:** System shall fetch current and historical (≥1 year) air quality data daily at 12:00 UTC
- **Input:** API credentials, target location
- **Output:** Structured dataset (CSV or database) with schema: `date, aqi, pm25, pm10, temperature, humidity, wind_speed`
- **Acceptance:** Data successfully stored; schema validated; missing values logged

### FR2: Data Cleaning & Feature Engineering
- **Requirement:** System shall transform raw data into analysis-ready format
- **Processing:**
  - Handle missing values via forward-fill or interpolation
  - Create lag features (previous day, previous week AQI)
  - Encode temporal features (day of week, month, season)
- **Acceptance:** Processed dataset has no null values; feature statistics match expectations

### FR3: Model Training
- **Requirement:** System shall train a regression model on cleaned data
- **Target variable:** Tomorrow's AQI or PM2.5
- **Algorithm:** scikit-learn model (Linear Regression, Random Forest, or Gradient Boosting)
- **Acceptance:** Model saved as artifact; performance metrics (MAE, RMSE, R²) computed and logged

### FR4: Prediction API
- **Requirement:** System shall expose a REST API to generate forecasts
- **Endpoint:** `GET /api/forecast`
- **Input:** Location (latitude, longitude)
- **Output:** JSON with `forecast_aqi`, `confidence_interval`, `recommendation`
- **Acceptance:** API responds in <500ms; predictions consistent across requests

### FR5: Web Dashboard
- **Requirement:** System shall display air quality in user-friendly format
- **Components:**
  - Current AQI (measured) with color-coded badge
  - Next-day forecast with confidence
  - 30-day historical chart
- **Interaction:** Dashboard auto-refreshes every hour
- **Acceptance:** Dashboard loads without errors; all data fresh and accurate

### FR6: Documentation
- **Requirement:** System shall include runbook and model documentation
- **Artifacts:** `RUNBOOK.md`, `MODEL_CARD.md`, inline code comments
- **Acceptance:** New user can reproduce setup in <1 hour

---

## 8. Non-Functional Requirements

### NFR1: Performance
- **Dashboard load time:** <2 seconds on 4G network
- **API response time:** <500 milliseconds
- **Model inference time:** <100 milliseconds per request
- **Measurement:** Use browser DevTools and load-testing tools (e.g., Apache JMeter)

### NFR2: Reliability
- **Uptime:** 95% (acceptable 1–2 hours downtime per month)
- **Data freshness:** Forecasts updated within 2 hours of data fetch
- **Graceful degradation:** If API fails, display last cached prediction with staleness warning
- **Measurement:** Automated uptime monitoring (e.g., UptimeRobot)

### NFR3: Usability
- **Target audience:** General public (age 18–65, varies in technical skill)
- **Device support:** Desktop and mobile browsers
- **Accessibility:** Sufficient color contrast; text descriptions for colors (e.g., "Moderate" labels alongside color coding)
- **Measurement:** Manual testing on Chrome, Firefox, Safari; WCAG AA compliance check

### NFR4: Maintainability
- **Code structure:** Modular functions in `src/`; minimal duplicated logic
- **Test coverage:** ≥70% of business logic covered by unit tests
- **Documentation:** Every module has docstrings; README explains architecture
- **Data contracts:** Schema versioning in `docs/DATA_SCHEMA.md`
- **Measurement:** Code review checklist; pytest coverage report

### NFR5: Scalability (Future Consideration)
- **Current scope:** Single city, <10K daily users
- **Future-ready design:** Parameterized city/region; no hard-coded coordinates
- **Database design:** Supports >1 year of daily data without significant slowdown

---

## 9. Success Metrics

### Model Performance Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Mean Absolute Error (MAE)** | <20 AQI points | Threshold where forecast errors don't mislead users |
| **Root Mean Squared Error (RMSE)** | <30 AQI points | Penalizes large misses; encourages consistency |
| **R² Score** | >0.70 | Model explains majority of variance; non-trivial relationship |
| **Coverage** | 95% of days have valid forecast | Missing predictions reduce utility |

### System Performance Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| **Dashboard load time** | <2 sec | Browser DevTools timing |
| **API latency** | <500 ms | Response time monitoring |
| **System uptime** | 95% | Automated pings; error aggregation |
| **Data freshness** | Latest data ≤2 hrs old | Timestamp in API response |

### Delivery Metrics

| Milestone | Target | Status |
|-----------|--------|--------|
| **Week 1:** Data pipeline ready | 100% | Data accessible, EDA complete |
| **Week 2:** Baseline model trained | 100% | Model artifact + performance logged |
| **Week 3:** End-to-end integration | 100% | Dashboard integrated with model predictions |
| **Week 4:** Production deployment | 100% | Live URL, documentation complete |

### User Engagement Metrics (Post-Launch, Optional)

- Number of unique daily users
- Average session duration
- Forecast accuracy as rated by user feedback
- Bounce rate on dashboard

---

## 10. Risks & Mitigation

### Risk 1: Data Availability/Quality

**Risk:** Air quality API is unavailable, returns incomplete data, or has rate limits.

**Probability:** Medium  
**Impact:** High (project cannot proceed without data)

**Mitigation:**
- Identify primary and backup data sources in Week 1 (e.g., OpenWeatherMap + government environmental agency)
- Download and cache 2+ years of historical data locally before sprint
- Implement retry logic with exponential backoff in data ingestion script
- Set up alerts for data feed anomalies (e.g., >50% missing values)

---

### Risk 2: Model Performance Below Acceptable Threshold

**Risk:** Forecast model achieves MAE >30 AQI points, reducing user trust.

**Probability:** Medium  
**Impact:** High (unusable product)

**Mitigation:**
- Start with simple baseline (persistence forecast: tomorrow = today) to establish lower bound
- Reserve Week 3 for model iteration; don't commit to complex algorithms early
- Use cross-validation to ensure generalization, not just train-set memorization
- If target not met by end of Week 3:
  - Simplify target (forecast category instead of numeric AQI)
  - Document model limitations on dashboard ("Forecast is exploratory; use with caution")
  - Plan model improvements for post-launch

---

### Risk 3: Scope Creep / Missed Deadlines

**Risk:** Team takes on additional features (multi-city, mobile app, real-time alerts), missing core deadline.

**Probability:** High  
**Impact:** Medium (incomplete delivery)

**Mitigation:**
- Strict scope freeze at Week 1 kickoff; all additions require team consensus + time trade-off analysis
- Daily standups to flag schedule slippage early
- Use GitHub Issues with priority labels; only work on "MVP" labels during sprint
- If running behind: remove one non-MVP feature rather than extending timeline
- Post-launch feature request doc for future iterations

---

### Risk 4: App Deployment Failure / Infrastructure Downtime

**Risk:** Deployment tooling is unfamiliar, or hosting platform has unexpected downtime.

**Probability:** Medium  
**Impact:** Medium (unable to test live; delayed launch)

**Mitigation:**
- Choose well-documented hosting platform with free tier (e.g., Heroku, Vercel, DigitalOcean)
- Deploy prototype app (dummy data) by end of Week 1, not Week 4
- Maintain local runnable version; use Docker for reproducible environments
- Set up uptime monitoring and have rollback procedure ready
- Candidate: Deploy to multiple platforms if time permits (redundancy)

---

### Risk 5: Team Knowledge Silos

**Risk:** Data engineer owns data pipeline; ML engineer owns model; app developer owns frontend. If someone leaves, knowledge is lost.

**Probability:** Low (4-week sprint)  
**Impact:** High (project stalls if key person unavailable)

**Mitigation:**
- Weekly cross-functional code reviews ensure all team members understand each layer
- Maintain comprehensive documentation (`RUNBOOK.md`, `MODEL_CARD.md`, architecture diagram)
- Pair programming on critical integration points (Week 3)
- Keep all code in version control; commit frequently with clear messages

---

### Risk 6: Feature Creep in Model

**Risk:** ML engineer spends weeks on feature engineering, hyperparameter tuning, or trying advanced algorithms, delaying deployment.

**Probability:** Medium  
**Impact:** Medium (delays other work)

**Mitigation:**
- Set a "time box" for feature engineering: maximum 1 day per experiment
- Define "done" criteria early: MAE <20 is acceptable; don't optimize forever for MAE <15
- Use simple first: start with top 5 features; add only if model performance stalls
- Automated experiment tracking (e.g., MLflow) to avoid re-running failed experiments

---

### Risk 7: Misunderstanding of Problem / User Expectations

**Risk:** After deployment, users ask "Why can't I get a 7-day forecast?" or "Why isn't this multi-city?"

**Probability:** Medium  
**Impact:** Low–Medium (reduced adoption, but no rework needed mid-sprint)

**Mitigation:**
- Document out-of-scope items in README with rationale
- Show prototype to stakeholder in Week 2 for feedback before full build-out
- On launch page, set expectations: "Current MVP: 1-day forecast, single city"
- Collect feature requests post-launch; prioritize for next iteration

---

### Risk 8: Data Quality / Seasonal Biases

**Risk:** Model trained on data from one season performs poorly in another season.

**Probability:** Medium  
**Impact:** Medium (forecast degrades during unseen seasons)

**Mitigation:**
- Validate that historical dataset spans at least one full year
- Use time-series cross-validation (not random train/test split) to detect temporal bias
- Monitor model performance separately by season post-launch
- Include seasonal ARIMA or trend-based baseline for comparison
- Document known limitations on dashboard if bias detected

---

### Risk 9: Security / Privacy

**Risk:** App exposes sensitive user data or is vulnerable to attacks (though low risk for MVP).

**Probability:** Low  
**Impact:** High (legal liability)

**Mitigation:**
- No user authentication required for MVP (public dashboard)
- Use HTTPS for all API communication
- Store API credentials in environment variables, not in code
- Basic input validation on API requests (sanitize location parameters)
- Dependency scanning for known vulnerabilities (e.g., `pip audit`, Snyk)

---

## Execution Checklist

### Pre-Sprint (End of Week 0)

- [ ] Team roles assigned
- [ ] Target city chosen; data sources confirmed
- [ ] GitHub repo initialized with project structure
- [ ] Development environments set up and tested
- [ ] Kick-off meeting completed; all stakeholders aligned

### Post-Sprint (End of Week 4)

- [ ] All functional requirements met
- [ ] Non-functional requirements validated
- [ ] Model performance on test set within acceptable range
- [ ] Deployment successful; live URL accessible
- [ ] Full documentation (RUNBOOK, MODEL_CARD, code comments) complete
- [ ] Team retrospective completed; lessons documented

---

## Appendix: References & Tools

### Suggested Tools

- **Data:** pandas, NumPy, scikit-learn
- **Web:** Flask or FastAPI (backend), HTML/CSS/JavaScript (frontend)
- **Deployment:** Heroku, DigitalOcean, AWS (choose one for simplicity)
- **Monitoring:** Sentry (errors), UptimeRobot (uptime), CloudWatch (logs)
- **Version Control:** Git + GitHub; branch-per-feature workflow

### Helpful Resources

- AQI Standards: https://www.airnow.gov/aqi/aqi-basics/
- OpenWeatherMap API: https://openweathermap.org/api
- scikit-learn documentation: https://scikit-learn.org/stable/

---

**Document Status:** Active  
**Last Reviewed:** April 1, 2026  
**Next Review:** Weekly (Friday standup)
