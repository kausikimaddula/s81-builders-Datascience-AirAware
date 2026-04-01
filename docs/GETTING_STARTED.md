# AirAware: Project Overview & Getting Started

**Project Status:** Active Development (4-Week Sprint)  
**Start Date:** [TBD]  
**Target Delivery:** Week 4 (Day 28)  

---

## 🎯 What is AirAware?

AirAware is a data science project that helps citizens understand local air pollution trends and predict next-day air quality to support safer outdoor planning.

**Core Problem:** Citizens lack accessible, predictive information about air quality.  
**Core Solution:** Web dashboard with real-time data + next-day AQI forecast.

---

## 📚 Documentation Roadmap

**Start here depending on your role:**

### For Project Managers & Product Leads
1. **[PROJECT_PLAN.md](PROJECT_PLAN.md)** — Full 4-week sprint plan with timeline, roles, risks, and success metrics.
2. **[docs/RUNBOOK.md](docs/RUNBOOK.md)** — How to deploy and monitor the completed system.

### For Data Engineers
1. **[docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md)** — Raw data sources, schemas, and quality standards.
2. **[docs/RUNBOOK.md](docs/RUNBOOK.md#4-fetch-data)** — Data fetching and preparation commands.
3. **[PROJECT_PLAN.md#2-dataset-selection--scope](PROJECT_PLAN.md#2-dataset-selection--scope)** — Context on why this dataset was chosen.

### For ML Engineers
1. **[docs/MODEL_CARD.md](docs/MODEL_CARD.md)** — Template for documenting model architecture, performance, and limitations.
2. **[PROJECT_PLAN.md#9-success-metrics](PROJECT_PLAN.md#9-success-metrics)** — Model performance targets (MAE <20, R² >0.70).
3. **[docs/RUNBOOK.md#6-train-the-model](docs/RUNBOOK.md#6-train-the-model)** — Training and inference commands.

### For App/Backend Developers
1. **[docs/RUNBOOK.md#8-run-the-web-dashboard](docs/RUNBOOK.md#8-run-the-web-dashboard)** — Setting up and running the Flask app.
2. **[docs/RUNBOOK.md#10-deploy-to-production](docs/RUNBOOK.md#10-deploy-to-production)** — Deploying to Heroku or DigitalOcean.
3. **[PROJECT_PLAN.md#7-functional-requirements](PROJECT_PLAN.md#7-functional-requirements)** — What the API and dashboard must do.

### For New Contributors
1. **[README.md](README.md)** — High-level project intent and lifecycle.
2. **[docs/repository-review-checklist.md](docs/repository-review-checklist.md)** — Structured checklist for understanding the project.
3. **[docs/folder-lifecycle-map.md](docs/folder-lifecycle-map.md)** — Folder organization and change boundaries.

---

## 📂 Folder Structure (& When to Use Each)

```
AirAware/
├── README.md                    # High-level project overview
├── PROJECT_PLAN.md              # Full 4-week sprint plan with all 9 sections
├── requirements.txt             # Python dependencies
│
├── data/
│   ├── raw/                     # Source data (never edit directly)
│   └── processed/               # Clean, feature-engineered data for modeling
│
├── notebooks/
│   ├── 01_repo_intent_review.ipynb      # Read this first to understand project
│   ├── 02_eda.ipynb             # Exploratory data analysis (to be created)
│   └── 03_model_experiments.ipynb       # Model iteration and tuning (to be created)
│
├── src/
│   ├── fetch_data.py            # API data ingestion
│   ├── prepare_data.py           # Data cleaning, feature engineering
│   ├── train_model.py            # Model training and evaluation
│   ├── inference.py              # Single-record prediction
│   └── config.py                 # Shared configuration
│
├── models/
│   └── aqi_forecast_v1.0.pkl    # Trained model artifact (to be created)
│
├── app/
│   ├── app.py                    # Flask backend
│   └── frontend/                 # HTML/CSS/JS dashboard (optional)
│
├── reports/
│   └── figures/                  # Final charts for reports
│
├── tests/
│   ├── test_data.py              # Unit tests for data functions
│   ├── test_model.py             # Unit tests for ML logic
│   └── integration_test.py        # End-to-end pipeline test
│
├── outputs/
│   ├── model_metrics.json        # Model performance (to be created)
│   └── predictions.csv           # Batch predictions (to be created)
│
└── docs/
    ├── repository-review-checklist.md       # Checklist: Read before contributing
    ├── readme-audit-template.md             # Template: Audit documentation quality
    ├── folder-lifecycle-map.md              # Folder roles and change boundaries
    ├── DATA_SCHEMA.md                       # Raw & processed data contracts
    ├── MODEL_CARD.md                        # Model documentation template
    ├── RUNBOOK.md                           # Setup & deployment guide
    └── ARCHITECTURE.md                      # System design (to be created)
```

---

## 🚀 Quick Start for New Team Members

### 1. Read the Project Context (15 minutes)

- Start: [README.md](README.md)
- Then: [docs/repository-review-checklist.md](docs/repository-review-checklist.md)

### 2. Set Up Your Environment (20 minutes)

```bash
git clone https://github.com/your-org/AirAware.git
cd AirAware
python -m venv venv
source venv/bin/activate  # or `. venv/bin/activate` on Windows
pip install -r requirements.txt
```

### 3. Review the Project Plan by Role (30 minutes)

- **All roles:** Read [PROJECT_PLAN.md](PROJECT_PLAN.md) sections 1–5 (problem, data, roles, timeline, deployment)
- **Your specific role:** Read relevant sections:
  - Data Engineering → Section 2 (Dataset Selection), Section 5 (Deployment testing)
  - ML Engineering → Section 9 (Success Metrics)
  - App Development → Section 7 (Functional Requirements)

### 4. Week 1 Kick-Off (Check the Timeline)

Refer to [PROJECT_PLAN.md#4-sprint-timeline-4-weeks](PROJECT_PLAN.md#4-sprint-timeline-4-weeks) for your specific week's tasks.

---

## 📋 Weekly Milestones

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| **Week 1** | Foundation | Data pipeline validated, EDA complete |
| **Week 2** | Preparation | Clean data + baseline model ready |
| **Week 3** | Integration | Model integrated with app, end-to-end test passing |
| **Week 4** | Finalization | Production deployment, full documentation |

**See [PROJECT_PLAN.md#4-sprint-timeline-4-weeks](PROJECT_PLAN.md#4-sprint-timeline-4-weeks) for detailed day-by-day breakdown.**

---

## 🎯 Success Criteria

Your project is **complete** when:

1. ✅ **Model Performance:** MAE <20 AQI points, R² >0.70 on test set
2. ✅ **System Performance:** Dashboard loads in <2 sec, API responds in <500ms
3. ✅ **Deployment:** Live and accessible at public URL (e.g., Heroku)
4. ✅ **Documentation:** README, RUNBOOK, and Model Card complete + accurate
5. ✅ **Reproducibility:** New user can set up and run pipeline in <1 hour following [RUNBOOK.md](docs/RUNBOOK.md)

**See [PROJECT_PLAN.md#9-success-metrics](PROJECT_PLAN.md#9-success-metrics) for full metrics.**

---

## ⚠️ Key Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Data source unavailable | Confirm API access + download 1 year history in Week 1 |
| Model performance below threshold | Reserve Week 3 for iteration; simplify target if needed |
| Scope creep | Weekly scope freeze check; prioritize MVP only |
| Deployment failure | Deploy dummy app by Week 1; use Docker for reproducibility |
| Team knowledge silos | Cross-functional code reviews, pair programming |

**See [PROJECT_PLAN.md#10-risks--mitigation](PROJECT_PLAN.md#10-risks--mitigation) for all risks + detailed mitigations.**

---

## 📞 Communication Guidelines

- **Weekly Standup:** Friday 10:00 AM (15 min) — blockers, progress, help needed
- **Slack Channel:** #airaware-dev
- **Documentation Updates:** When critical decisions are made, update relevant `docs/*.md` files
- **Code Reviews:** All PRs reviewed before merge; checklist: [docs/PR_CHECKLIST.md](docs/PR_CHECKLIST.md) (to be created)

---

## 🔗 External Resources

- **Air Quality Data:**
  - OpenWeatherMap Air Pollution API: https://openweathermap.org/api/air-pollution
  - AQI Standards: https://www.airnow.gov/aqi/aqi-basics/

- **ML & Data Science:**
  - scikit-learn docs: https://scikit-learn.org/stable/
  - Time-series model evaluation: https://www.machinelearningplus.com/time-series/

- **Deployment:**
  - Heroku docs: https://devcenter.heroku.com/
  - Docker docs: https://docs.docker.com/

---

## 📝 Checklist: Before Your First Code Commit

- [ ] I have read [README.md](README.md) and understand the problem
- [ ] I have read [PROJECT_PLAN.md](PROJECT_PLAN.md) Section 1–5 (all roles)
- [ ] I have read [PROJECT_PLAN.md](PROJECT_PLAN.md) sections relevant to my role
- [ ] I have set up my local environment following [docs/RUNBOOK.md#2-set-up-python-environment](docs/RUNBOOK.md#2-set-up-python-environment)
- [ ] I have read [docs/folder-lifecycle-map.md](docs/folder-lifecycle-map.md) and understand change boundaries
- [ ] I have a clear first task identified from [PROJECT_PLAN.md#4-sprint-timeline-4-weeks](PROJECT_PLAN.md#4-sprint-timeline-4-weeks)
- [ ] I know where to ask questions (Slack, weekly standup)

---

## 🎬 Next Steps

1. **If you are new to the project:**
   - Read [README.md](README.md) (5 min)
   - Complete [docs/repository-review-checklist.md](docs/repository-review-checklist.md) (20 min)

2. **If you are joining a sprint in progress:**
   - Review [PROJECT_PLAN.md#4-sprint-timeline-4-weeks](PROJECT_PLAN.md#4-sprint-timeline-4-weeks) for current week
   - Check the GitHub issue board for available tasks
   - Pair with a team member on an active task

3. **If you are running this project:**
   - Use [docs/RUNBOOK.md](docs/RUNBOOK.md) to set up a clean environment
   - Refer to [PROJECT_PLAN.md](PROJECT_PLAN.md) for checkpoint dates and deliverables
   - Share this document with all team members

---

**Questions?** Ask in Slack (#airaware-dev) or open a GitHub issue.  
**Last Updated:** April 1, 2026
