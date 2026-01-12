# Tasks: Company Profile Directory

**Feature Branch**: `001-company-directory`
**Spec**: [spec.md](spec.md)

## Phase 1: Setup

*Goal: Initialize the new app and infrastructure.*

- [x] T001 Create `companies` app using `python manage.py startapp companies`
- [x] T002 Register `orgtorii.companies` in `INSTALLED_APPS` in `orgtorii/orgtorii/settings.py`
- [x] T003 Create `orgtorii/companies/urls.py` with empty `urlpatterns`
- [x] T004 Include `companies.urls` in root `orgtorii/orgtorii/urls.py`

## Phase 2: Foundational (Models)

*Goal: Implement the data model to support all user stories.*

- [x] T005 [P] Implement `Industry` model with UUID in `orgtorii/companies/models.py`
- [x] T006 [P] Implement `Company` model with UUID and `is_stub` logic in `orgtorii/companies/models.py`
- [x] T007 [P] Implement `CompanyWebsite` model in `orgtorii/companies/models.py`
- [x] T008 [P] Implement `CompanyUser` model with roles (ADMIN, EDITOR, READ_ONLY) in `orgtorii/companies/models.py`
- [x] T009 [P] Implement `CompanyRevision` model with JSON snapshot field in `orgtorii/companies/models.py`
- [x] T010 Create and run migrations for `companies` app

## Phase 3: User Story 1 - Create New Company Profile (P1)

*Goal: Allow contributors to add new companies.*

- [x] T011 [US1] Implement `CompanyForm` in `orgtorii/companies/forms.py` (fields: name, industry, description, hq_location)
- [x] T012 [US1] Implement `CompanyCreateView` in `orgtorii/companies/views.py` with automatic slug generation
- [x] T013 [US1] Create template `orgtorii/templates/companies/company_form.html`
- [x] T014 [US1] Register `/companies/create/` in `orgtorii/companies/urls.py`
- [x] T015 [US1] Implement tests for company creation in `orgtorii/companies/tests/test_views.py`

## Phase 4: User Story 4 - View Company Profile (P1)

*Goal: Publicly display company information.*

- [x] T016 [US4] Implement `CompanyDetailView` in `orgtorii/companies/views.py`
- [x] T017 [US4] Create template `orgtorii/templates/companies/company_detail.html` (display all fields + websites)
- [x] T018 [US4] Implement `CompanyListView` with pagination and search in `orgtorii/companies/views.py`
- [x] T019 [US4] Create template `orgtorii/templates/companies/company_list.html`
- [x] T020 [US4] Register list and detail URLs in `orgtorii/companies/urls.py`
- [x] T021 [US4] Implement tests for list and detail views in `orgtorii/companies/tests/test_views.py`

## Phase 5: User Story 2 - Edit Company Details (P1)

*Goal: Allow updates and revision tracking.*

- [x] T022 [US2] Update `CompanyForm` to support inline `CompanyWebsite` management (using formsets)
- [x] T023 [US2] Implement revision creation logic (signal or service) in `orgtorii/companies/services.py` that snapshots data on save
- [x] T024 [US2] Implement `CompanyUpdateView` in `orgtorii/companies/views.py`
- [x] T025 [US2] Register `/companies/<slug>/edit/` in `orgtorii/companies/urls.py`
- [x] T026 [US2] Update `company_detail.html` to link to edit view
- [x] T027 [US2] Implement tests for editing and revision snapshot creation in `orgtorii/companies/tests/test_views.py`

## Phase 6: User Story 3 - View Revision History & Rollback (P2)

*Goal: History visibility and restoration.*

- [x] T028 [US3] Implement `CompanyHistoryView` in `orgtorii/companies/views.py`
- [x] T029 [US3] Create template `orgtorii/templates/companies/company_history.html`
- [x] T030 [US3] Implement `CompanyRevertView` logic (apply snapshot to current instance) in `orgtorii/companies/views.py`
- [x] T031 [US3] Register history and revert URLs in `orgtorii/companies/urls.py`
- [x] T032 [US3] Implement tests for history view and revert functionality in `orgtorii/companies/tests/test_views.py`

## Phase 7: User Story 5 - Manage Official Users (P2)

*Goal: Permissions and role management.*

- [ ] T033 [US5] Implement `IsCompanyAdmin` and `IsCompanyEditor` permission mixins in `orgtorii/companies/permissions.py`
- [ ] T034 [US5] Apply permissions to Update and Revert views in `orgtorii/companies/views.py`
- [ ] T035 [US5] Implement `CompanyUserManageView` to add/remove users and change roles in `orgtorii/companies/views.py`
- [ ] T036 [US5] Create template `orgtorii/templates/companies/company_users.html`
- [ ] T037 [US5] Register management URL in `orgtorii/companies/urls.py`
- [ ] T038 [US5] Implement tests for permissions and user management in `orgtorii/companies/tests/test_permissions.py`

## Phase 8: Polish

*Goal: Final cleanup and UX improvements.*

- [x] T039 Polish templates with Tailwind CSS (ensure mobile responsiveness)
- [x] T040 Verify "Is Stub" logic visual indicators in templates
- [x] T041 Ensure SEO tags (title, meta description) are correct in `company_detail.html`
- [x] T042 Run full test suite `just test-unit orgtorii.companies`

## Dependencies

- Phase 1 & 2 must be completed before any User Story phases.
- Phase 3 (Create) and Phase 4 (View) can be done in parallel.
- Phase 5 (Edit) depends on Phase 3 (Create) and Phase 2 (Models).
- Phase 6 (History) depends on Phase 5 (Edit) for generating revisions.
- Phase 7 (Users) can be done after Phase 2, but makes most sense after Phase 5 to protect the edit routes.

## Implementation Strategy

1. **MVP Scope**: Phases 1-5 deliver a working directory where any logged-in user can contribute (assuming loose permissions for P1).
2. **Full Feature**: Phases 6-7 add the necessary governance and history features for a "Wiki" style system.
