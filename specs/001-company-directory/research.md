# Research & Decisions: Company Profile Directory

**Status**: Complete
**Date**: 2026-01-12

## 1. Data Model Strategy

### Decision: Separate `Company` App

We will create a new Django app named `companies` rather than reusing the existing `organizations` app.

**Rationale**:

- The existing `organizations.Organisation` model is designed for SaaS multi-tenancy (RBAC, billing, members).
- The `Company` profile is a public, "Wikipedia-style" directory entity.
- Separation of concerns allows the public directory to evolve independently of the SaaS logic.
- Future integration (claiming a page) can be modeled as a link between an `Organisation` (tenant) and a `Company` (profile).

### Decision: Manual Revision History

We will implement a custom `CompanyRevision` model instead of using `django-reversion`.

**Rationale**:

- **Clean Data Dumps**: The spec requires strict separation of public company info and private user metadata for daily dumps. A custom model gives us exact control over the schema to ensure no private data leaks into the "snapshot".
- **Grug Brain**: A simple model with a JSON snapshot is easier to understand, query, and debug than a generic third-party library wrapper.
- **Specific Requirements**: We need to track "Is Stub" and specific field changes which are easier to handle explicitly.

## 2. Technology Stack

### Decision: Django + Vanilla/Tailwind

We will use standard Django templates with Tailwind CSS (via the existing build system) and minimal vanilla JS.

**Rationale**:

- **Simplicity**: Avoids the complexity of a separate SPA for a content-heavy, SEO-critical directory.
- **Performance**: Server-side rendering is optimal for "Wikipedia-style" content.
- **Consistency**: Matches the "Grug Brain" philosophy of the project.

## 3. Unknowns & Clarifications

### Resolved: User Attribution

- **Question**: How to link anonymous/public edits?
- **Resolution**: The `CompanyRevision` model will have a nullable `editor` field (ForeignKey to `User`). If we allow anonymous edits in the future, we can add a session ID or IP hash, but for now, the spec implies "Contributors" are users. We will assume logged-in users for P1 stories based on "As a contributor" phrasing.

### Resolved: Slug Uniqueness

- **Question**: How to handle "Acme"?
- **Resolution**: Standard Django slugification with a numeric suffix counter loop on save (e.g., `acme`, `acme-1`).
