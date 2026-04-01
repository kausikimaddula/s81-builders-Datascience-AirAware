# AirAware: Repository Reading and Contribution Milestone

This repository is designed to train a core data science skill: reading a project as a story, not just a set of files.

The goal of this milestone is to help contributors understand intent before implementation.

## 1. A Repository Is a Story, Not Just Files

Use these guiding questions before making changes:

1. What problem is this project trying to solve?
2. How does the structure reflect the data science lifecycle?
3. What work is already complete, and what assumptions does it rely on?

For AirAware, the core problem is:

How can citizens better understand air pollution trends and anticipate health risks in their city?

This keeps the project focused on decision support rather than model-building without context.

## 2. README as the Project Entry Point

A strong README should communicate:

1. Problem statement and intended user impact
2. Dataset sources and quality considerations
3. Workflow from data ingestion to insight generation
4. Main outputs and key takeaways
5. How to run or explore the project

This repository now includes templates and checklists in [docs/repository-review-checklist.md](docs/repository-review-checklist.md) and [docs/readme-audit-template.md](docs/readme-audit-template.md) to evaluate whether documentation is complete.

## 3. Folder Structure and Lifecycle Mapping

Folder names are less important than lifecycle intent. The structure below maps to common data science stages:

- [data/raw/](data/raw/): source-aligned files, never manually edited
- [data/processed/](data/processed/): cleaned or transformed datasets
- [notebooks/](notebooks/): exploration, hypothesis testing, and narrative analysis
- [src/](src/): reusable code for ingestion, cleaning, and modeling
- [reports/figures/](reports/figures/): finalized charts used in communication
- [docs/](docs/): project intent, assumptions, review notes, and contribution guidance

See [docs/folder-lifecycle-map.md](docs/folder-lifecycle-map.md) for responsibilities and change boundaries.

## 4. Reading Notebooks and Code with Purpose

When reviewing notebooks or scripts, focus on flow before syntax details:

1. Where data is loaded and from which source
2. How missing values and data quality issues are handled
3. What transformations produce analysis-ready features
4. Which sections are exploratory vs. final
5. How findings connect back to the original question

A starter notebook is provided at [notebooks/01_repo_intent_review.ipynb](notebooks/01_repo_intent_review.ipynb) to support structured repository review.

## 5. Assumptions, Limitations, and Open Questions

Critical review means identifying what is implied but not yet proven.

Typical checks for this project:

1. Are air quality and weather data sources available and reliable?
2. Is the health risk definition explicit and justified?
3. Are there missing data periods, sampling issues, or location bias?
4. Are evaluation metrics aligned with user decisions?
5. What important questions remain unresolved?

Use [docs/repository-review-checklist.md](docs/repository-review-checklist.md) to document findings consistently.

## 6. How This Milestone Prepares You to Contribute

By following this milestone process, contributors can:

1. Extend analysis without breaking existing workflows
2. Avoid duplicate work by understanding what already exists
3. Improve documentation where intent is unclear
4. Ask stronger, evidence-based questions in review discussions

## Recommended Contributor Workflow

1. Read this README fully
2. Complete the template in [docs/readme-audit-template.md](docs/readme-audit-template.md)
3. Walk through repository stages using [docs/folder-lifecycle-map.md](docs/folder-lifecycle-map.md)
4. Capture assumptions and gaps using [docs/repository-review-checklist.md](docs/repository-review-checklist.md)
5. Start new work in an additive way (new notebook or script) before refactoring existing artifacts

## Current Repository State

This repository is currently focused on interpretation and contribution readiness.

- Documentation and review structure: available
- Executable pipeline code: starter layout only
- Data files and model outputs: not committed in this milestone

That is intentional for this phase. The objective is to build strong repository-reading behavior before expanding implementation.


