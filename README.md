# 🌍 AirAware — Data Science Repo Readme (Question → Data → Insight)

This repository currently documents the **thinking and intent** behind an air-quality data science project called **AirAware**.

The milestone for this PR is about demonstrating that you can **read what exists, infer intent, and identify gaps** before writing code. This README is written to help a new contributor understand (1) what the project is trying to do, (2) how work would flow through a typical data-science lifecycle, and (3) what’s missing / still undecided.
## 📋 Quick Links

- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** — Comprehensive 4-week sprint plan with all 9 planning sections: problem statement, dataset selection, roles, timeline, deployment, MVP, requirements, success metrics, and risk mitigation.
- **[docs/repository-review-checklist.md](docs/repository-review-checklist.md)** — Checklist for understanding project intent before contributing.
- **[docs/readme-audit-template.md](docs/readme-audit-template.md)** — Template for auditing documentation completeness.
- **[docs/folder-lifecycle-map.md](docs/folder-lifecycle-map.md)** — Folder-to-lifecycle mapping and change boundaries.
- **[notebooks/01_repo_intent_review.ipynb](notebooks/01_repo_intent_review.ipynb)** — Interactive notebook for structured repository review.
---

## 1) Project Intent & High-Level Flow

### What problem is AirAware trying to address?

AirAware aims to help **citizens understand air pollution trends** and **anticipate potential health-risk conditions** in their city.

The underlying question is:

> **How can citizens better understand air pollution trends and anticipate health risks in their city?**

This frames the project as **decision support** (inform safer outdoor timing, risk awareness) rather than “build a model for its own sake.”

### What high-level workflow does the repository imply?

Even though this repo does not yet contain datasets, notebooks, or pipelines, the documented workflow is a standard data-science loop:

1. **Question (problem framing)**
   - Define the user, decision, scope, and what “success” means.
2. **Data (evidence gathering & validation)**
   - Identify sources (air quality + weather), collect, and evaluate quality/bias.
3. **Insight (analysis → communication → action)**
   - Translate patterns into recommendations and (optionally) forecasts.

If/when this becomes an executable project, the typical next steps would extend the “Data → Insight” stage into:

- Ingestion (API pulls / historical downloads)
- Cleaning & feature engineering (time-based features, lag features, meteorology joins)
- Exploratory analysis (seasonality, events, missingness)
- Modeling (forecast AQI/PM, classification of risk days, etc.)
- Evaluation (backtesting, error metrics, stability)
- Reporting (plots, dashboards, written takeaways)

### How does the current repository reflect lifecycle stages?

Right now, the repository reflects **only the earliest lifecycle stage**: problem framing.

- The “Question → Data → Insight” framing shows the project is deliberately starting with intent and decision-making.
- There is **no implemented “Data” layer** (no raw/processed datasets, no ingestion scripts) and **no “Insight” artifacts** (no notebooks/reports).

That’s not “wrong” for a milestone focused on reading/reasoning—just important context for contributors.

---

## 2) Repository Structure & File Roles

### What exists today (current structure)

- `README.md`: The only project artifact in the repository. It documents the project intent and a conceptual workflow.
- `.git/`: Version control metadata.

### How exploratory work vs finalized analysis is represented here

At the moment, exploratory and finalized analysis are **not present**. In a more complete data-science repo, you would usually see:

- **Exploratory work**: messy, iterative notebooks; lots of plots; quick sanity checks; competing hypotheses.
- **Finalized analysis**: reproducible scripts/notebooks; stable data contracts; clear outputs; documented assumptions; consistent run steps.

This repo is currently **pre-analysis** (documentation and intent only).

### Where a new contributor should be cautious

Since the README is currently the “source of truth,” changes here can unintentionally shift scope.

Be especially careful when modifying:

- The **main question** (it changes what data and modeling choices make sense)
- The **definition of “health risk”** (this impacts labeling, thresholds, and ethics)
- Any implied **data sources** (availability, licensing, rate limits, geography)

If you want to extend the project, it’s safer to **add new work** (new notebook, new script, new doc) rather than rewriting the problem statement.

---

## 3) Assumptions, Gaps, and Open Questions

### Assumptions implied by the current documentation

- **Air quality and weather data are available** for the target city (via government/environmental APIs, weather APIs, etc.).
- **AQI/PM measures map meaningfully to “health risk”** for the intended audience.
- **Forecasting is useful** (users gain value from predicted risk levels, not only historical trends).
- The project is city-based and assumes a consistent **location/time index** for joins.

### Gaps / unclear steps (what a contributor can’t yet infer)

- **Data source decision**: Which API(s)? What historical coverage? What licensing/terms?
- **Scope**: Which city/cities? Single city MVP vs multi-city generalization?
- **Target & evaluation**: What exactly is predicted (AQI, PM2.5, risk category)? What metric defines “good”?
- **Definition of “health risk”**: Which standard (e.g., AQI categories) and what user guidance is appropriate?
- **Reproducibility**: No environment spec, run steps, or pipeline conventions exist yet.

### One concrete improvement to make the repo easier to extend

Add a minimal “execution skeleton” that turns intent into a reproducible workflow. For example:

- A `data/` folder with a short `data/README.md` describing the intended sources and schemas.
- A `notebooks/` folder for exploration (numbered notebooks).
- A `src/` (or `scripts/`) folder for reusable code (ingestion, cleaning, features).
- An `outputs/` folder for generated charts/reports (kept out of git if large).
- A `requirements.txt` (or `environment.yml`) to make runs reproducible.

This improvement is valuable because it separates exploratory work from stable components and reduces the chance a new contributor “breaks” others’ work.

---

## Contributor Decision-Making (How to Extend Without Breaking Things)

If you are asked to add a new analysis but you’re unsure where to start:

1. **Start from the question**
   - Confirm the user decision you’re supporting (trend awareness? next-week forecast? high-risk alerts?).
2. **Add work in an isolated place first**
   - Create a new notebook for exploration, or a new script that does not change existing artifacts.
3. **Treat data contracts as stable once established**
   - When a dataset schema is agreed upon, avoid “quietly” changing column meanings/types without updating docs.
4. **Promote only what’s reproducible**
   - Move reusable logic from notebooks into scripts/modules only after it’s validated.
5. **Prefer additive PRs**
   - New files and new outputs are safer than refactoring the original intent.

---

## Video Walkthrough (≈2 Minutes) — Suggested Script

Use this as a checklist so your video includes reasoning, not just a file tour.

**0:00–0:20 — Show the repo structure**

- “This repo is minimal: it currently contains a single README that documents project intent.”
- “That tells me the project is in the *problem framing* stage, not the implementation stage.”

**0:20–1:05 — Explain intent + flow (Question → Data → Insight)**

- “The core question is about helping citizens understand pollution trends and anticipate risk.”
- “The workflow implied is: define the question, gather/evaluate data (air quality + weather), then produce insights and potentially forecasts.”
- “This README helps by clarifying purpose before modeling.”

**1:05–1:35 — Explain what’s missing / open questions**

- “There are no data sources chosen yet, no notebook outputs, and no reproducible run steps.”
- “The biggest open question is how ‘health risk’ is defined and evaluated.”

**1:35–2:00 — Scenario-based reasoning (mandatory)**

- “If I needed to add a new analysis without breaking work, I’d start with an additive notebook or script and avoid changing the problem statement.”
- “I’d use documentation to decide what to leave untouched (the core question/assumptions) and what to extend (new analysis artifacts, new data ingestion code once sources are chosen).”


