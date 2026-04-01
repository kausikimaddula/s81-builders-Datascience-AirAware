# Folder Lifecycle Map

This document explains what each folder represents in the data science lifecycle and how contributors should use it.

## Lifecycle Stages

1. Problem framing
2. Data acquisition
3. Data preparation
4. Exploration and analysis
5. Modeling and evaluation
6. Communication and reporting

## Folder Responsibilities

### data/raw/

- Purpose: Store unmodified source data.
- Rule: Treat as immutable snapshots.
- Do not: Manually clean or edit files in place.

### data/processed/

- Purpose: Store cleaned and transformed datasets.
- Rule: Generate from scripts or notebooks, not by manual edits.
- Do not: Mix processed files with raw source files.

### notebooks/

- Purpose: Exploration, quick tests, and narrative analysis.
- Rule: Number notebooks to indicate progression.
- Do not: Hide critical production logic only inside notebooks.

### src/

- Purpose: Reusable code for ingestion, transformations, and modeling.
- Rule: Move stable logic here once validated.
- Do not: Duplicate reusable functions across many notebooks.

### reports/figures/

- Purpose: Final visual artifacts used for communication.
- Rule: Keep outputs curated and easy to reference.
- Do not: Store transient debug images as final figures.

### docs/

- Purpose: Intent, assumptions, and contributor guidance.
- Rule: Update docs when project direction changes.
- Do not: Let documentation drift behind implementation.

## Change Boundaries for New Contributors

- Safe first changes: new notebook, new script, checklist updates, missing documentation.
- Risky changes: redefining targets, changing data contracts, replacing baseline metrics without justification.
- Required with risky changes: explicit rationale and updated documentation.
