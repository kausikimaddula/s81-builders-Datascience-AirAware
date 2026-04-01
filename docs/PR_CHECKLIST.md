# Pull Request Checklist

Use this checklist for all PRs to ensure code quality, documentation, and alignment with project goals.

**PR Title:** [Brief description]  
**Author:** [Your name]  
**Issue Link:** [Link to GitHub issue, if applicable]  
**Target Branch:** `main`  

---

## Code Quality

- [ ] Code follows PEP 8 / project style guide
  - Run: `black --line-length 100 src/`
  - Run: `flake8 src/`
- [ ] No unnecessary console logs or debug print statements
- [ ] Meaningful variable and function names (no `x`, `y`, `tmp`)
- [ ] Function docstrings included (describe purpose, inputs, outputs)
- [ ] Comments for complex logic

---

## Testing

- [ ] New code includes unit tests
- [ ] All existing tests pass locally
  - Run: `pytest tests/ -v`
- [ ] Test coverage for critical functions ≥70%
  - Run: `pytest tests/ --cov=src`
- [ ] Integration points tested (e.g., API→model→dashboard)

---

## Data & Models

- [ ] Data contract respected (no unexpected column additions/removals)
  - Check: [docs/DATA_SCHEMA.md](DATA_SCHEMA.md)
- [ ] No hardcoded file paths; use `config.py` or environment variables
- [ ] Model artifact versioned if modified
  - Include version in filename: `models/aqi_forecast_v1.1.pkl`
- [ ] Model assumptions/limitations documented ([docs/MODEL_CARD.md](MODEL_CARD.md))

---

## Documentation

- [ ] README.md updated if behavior/setup changes
- [ ] Docstrings updated if function signatures change
- [ ] RUNBOOK.md updated if new setup steps added
- [ ] Model Card ([docs/MODEL_CARD.md](MODEL_CARD.md)) updated if model trained
- [ ] Inline comments for non-obvious logic

---

## Deployment & Performance

- [ ] No new external dependencies without team discussion
  - If added: Updated `requirements.txt` and justified in PR
- [ ] Backward compatible (no breaking changes without migration plan)
- [ ] Database migrations (if applicable) documented
- [ ] Performance impact considered (e.g., model inference time <500ms)

---

## Security & Environment

- [ ] No credentials, API keys, or passwords in code
  - Use `.env` file + environment variables
- [ ] No sensitive user data logged
- [ ] Input validation on API endpoints (e.g., location bounds, date parsing)
- [ ] Dependency versions locked (no `*` in requirements.txt)

---

## Lifecycle & Scope

- [ ] Changes align with [PROJECT_PLAN.md](../PROJECT_PLAN.md) scope
- [ ] MVP features prioritized over nice-to-haves
- [ ] Out-of-scope features not sneaked in (discuss if there's overlap)
- [ ] Existing code not refactored unless explicitly needed

---

## Project-Specific Checks

### For Data Preparation
- [ ] Data quality report included (nulls, duplicates, outliers)
- [ ] Transformation rationale documented
- [ ] Processed data validated against schema

### For Model Training
- [ ] Cross-validation used (not just random train/test)
- [ ] Baseline model performance documented for comparison
- [ ] Hyperparameter tuning methodology logged
- [ ] Test set performance metrics in PR description

### For API/Dashboard
- [ ] API endpoints tested with curl or Postman
- [ ] Error handling for missing/invalid data
- [ ] Response times acceptable (<500ms)
- [ ] Dashboard tested on Chrome, Firefox, Safari (if frontend)

---

## Self-Review Before Submitting

- [ ] I have reviewed my own code and it's ready for peers to see
- [ ] Commit messages are clear and descriptive
  - Example: `feat: add lag features for AQI forecasting` (not `fix stuff`)
- [ ] Branch is up-to-date with `main`
  - Run: `git pull origin main`
- [ ] No merge conflicts
- [ ] All tests pass locally

---

## Code Review Process

**Reviewer Checklist:**

- [ ] Code does what the PR description says
- [ ] No obvious bugs or logic errors
- [ ] Performance acceptable (no N² loops, unnecessary API calls)
- [ ] Testing is adequate
- [ ] No hardcoded values or brittle assumptions
- [ ] Comments and documentation clear

**Approval:**

- At least 1 approval required before merge
- 2 approvals recommended for model/data changes

---

## Common Blockers & How to Fix

| Issue | Fix |
|-------|-----|
| "Tests are failing" | Run `pytest tests/ -v` locally; fix before pushing |
| "Linting errors" | Run `black src/` and `flake8 src/` |
| "Missing docstrings" | Add `"""Describe what this does."""` to functions |
| "Requirements.txt out of date" | Update with `pip freeze > requirements.txt` |
| "Merge conflict" | Resolve locally: `git pull origin main; git merge --no-ff origin/main` |

---

## Deployment Notes

**After PR is merged:**

- [ ] Monitor error logs (Sentry) for crashes
- [ ] Check model inference performance in production
- [ ] Verify data freshness (if data pipeline changed)
- [ ] Confirm no performance regression in dashboards

---

## PR Template (Use This When Creating a PR)

```markdown
## Description
Brief description of changes.

## Motivation & Context
Why is this change needed? What problem does it solve?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Data/model improvement
- [ ] Documentation
- [ ] Refactor

## Related Issue
Closes #<issue_number>

## Testing
Steps to test locally:
1. ...
2. ...

## Checklist
- [ ] Code quality checks pass (black, flake8, pytest)
- [ ] Documentation updated
- [ ] Data schema respected (if applicable)
- [ ] Model assumptions documented (if applicable)
- [ ] No hardcoded credentials or sensitive data
- [ ] Performance impact assessed

## Screenshots / Outputs
[If applicable: paste model metrics, dashboard screenshots, etc.]
```

---

## Questions During Review?

- Comment directly on the code line
- Ask for clarification rather than assuming intent
- Be respectful and constructive

---

**Last Updated:** April 1, 2026
