# Implementation Plan: Company Profile Directory

**Branch**: `001-company-directory` | **Date**: 2026-01-12 | **Spec**: [specs/001-company-directory/spec.md](spec.md)
**Input**: Feature specification from `specs/001-company-directory/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build the foundational "Wikipedia" layer of Org Torii: a public, searchable directory of companies with a revision history system.
Technical approach uses a new Django app `companies` with a `Company` model for public data and `CompanyRevision` model for history, ensuring clean separation of data for public dumps. Frontend uses standard Django templates + Tailwind.

## Technical Context

**Language/Version**: Python 3.13+ (Django 5+)
**Primary Dependencies**: Django, Vite (Frontend build), Tailwind CSS
**Storage**: SQLite (Dev), PostgreSQL (Prod)
**Testing**: pytest (Backend), playwright (E2E)
**Target Platform**: Web Browser
**Project Type**: Web Application (Django Monolith with Vite asset bundling)
**Constraints**: Grug Brain Simplicity, Security First (Separation of public/private data)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Open Knowledge First**: PASS. Data model explicitly separates public Company info from private User metadata to enable safe, complete public dumps.
- **Verified yet Anonymous**: PASS. `CompanyRevision` tracks edits via user reference, allowing for future verification layers while keeping public data clean.
- **Fair Employer Engagement**: N/A. Foundational layer does not yet implement claiming/paying.
- **Grug Brain Simplicity**: PASS.
  - Creating a dedicated `companies` app avoids coupling with complex SaaS `organizations` logic.
  - Using a simple `CompanyRevision` model with JSON snapshots avoids heavy external dependencies like `django-reversion` and complex configuration.
  - Using standard Django templates avoids SPA complexity.
- **Security & Integrity**: PASS. Strict separation of concerns ensures no PII leakage in public datasets.

## Project Structure

### Documentation (this feature)

```text
specs/001-company-directory/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── urls.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
orgtorii/
├── companies/                 # NEW APP
│   ├── migrations/
│   ├── models.py              # Company, CompanyRevision
│   ├── views.py               # CRUD views
│   ├── urls.py                # URL patterns
│   ├── forms.py               # CompanyForm
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
└── templates/
    └── companies/             # NEW TEMPLATES
        ├── company_list.html
        ├── company_detail.html
        ├── company_form.html
        └── company_history.html
```

**Structure Decision**: A new Django app `companies` is created to handle the public directory, distinct from the SaaS `organizations` app.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |
