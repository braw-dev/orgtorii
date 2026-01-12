# Feature Specification: Company Profile Directory

**Feature Branch**: `001-company-directory`
**Created**: 2026-01-12
**Status**: Draft
**Input**: User description: "Create a specification for the "Company Profile Directory". This is the foundational "Wikipedia" layer of Org Torii. Goal: Build a public, searchable directory of companies that serves as the anchor for all future data (reviews, salaries). Requirements: - Users MUST be able to create a new Company profile if it doesn't exist. - Users MUST be able to edit existing Company details (Name, Website, HQ Location, Description, Industry). - The system MUST maintain a revision history of changes to company profiles (Wiki-style), allowing rollbacks if needed. - Each company MUST have a unique, SEO-friendly slug (e.g., /companies/acme-corp). - Include a "stub" status for companies created with minimal info, encouraging others to fill it in. - Data Structure: Designed for daily public dumps (clean separation of public company info vs. private user metadata). - Companies can have multiple URLs. - Industry should be its own model and a ForeignKey for normalisation. - Use UUID v7. - Companies can have multiple "official" users which can have different roles (Admin, Editor, Read Only)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Company Profile (Priority: P1)

As a contributor, I want to add a missing company to the directory so that I and others can view and review it later.

**Why this priority**: foundational step to populate the empty directory.

**Independent Test**: Can be tested by visiting the create page, submitting a form, and verifying the new page exists.

**Acceptance Scenarios**:

1. **Given** a contributor is on the "Add Company" page, **When** they enter a valid Company Name and submit, **Then** a new profile is created, a unique slug is generated, and they are redirected to the new profile.
2. **Given** a contributor enters a Company Name that conflicts with an existing slug (if applicable), **When** they submit, **Then** the system generates a unique suffix or handles the collision gracefully (e.g. `acme-corp-1`).
3. **Given** a contributor provides only the mandatory Name, **When** the profile is created, **Then** the company status is visually identified as a "Stub".

---

### User Story 2 - Edit Company Details (Priority: P1)

As a contributor, I want to update company details (Name, Websites, HQ, Description, Industry) so that the information remains accurate.

**Why this priority**: Essential for the "Wiki" nature of the platform; static data becomes stale.

**Independent Test**: Can be tested by editing an existing company and verifying the new data is displayed and persisted.

**Acceptance Scenarios**:

1. **Given** a contributor is viewing a Company Profile, **When** they navigate to the Edit interface and update the HQ Location or add multiple Websites, **Then** the public profile immediately reflects the new data.
2. **Given** a contributor selects an Industry from the normalized list (or creates a new one if allowed), **When** they save, **Then** the Company is linked to that Industry.

---

### User Story 3 - View Revision History & Rollback (Priority: P2)

As a reader or contributor, I want to see the history of changes and revert vandalism so that the data remains trustworthy.

**Why this priority**: Critical for community trust and data integrity in an open wiki system.

**Independent Test**: Can be tested by making changes, viewing the history list, and performing a rollback.

**Acceptance Scenarios**:

1. **Given** a company profile has been edited multiple times, **When** a user views the "History" tab, **Then** they see a chronological list of changes including timestamp, author (if public), and what fields changed.
2. **Given** a contributor views a past revision in the history, **When** they select "Restore", **Then** the company details (including Industry and Websites) revert to that version's values, and a new "Restoration" revision is added to the history.

---

### User Story 4 - Manage Official Users (Priority: P2)

As a Company Admin, I want to assign roles to other users so they can officially represent the company.

**Why this priority**: Allows for distributed management and verification layers.

**Independent Test**: Can be tested by an admin user adding another user and verifying their permissions.

**Acceptance Scenarios**:

1. **Given** I am an Admin for a Company, **When** I add a user by email with "Editor" role, **Then** they are linked to the company with that role.
2. **Given** I am a Reader, **When** I view the company, **Then** I cannot see or modify the list of official users.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a new Company entity with at least a Name.
- **FR-002**: System MUST automatically generate a unique, URL-friendly slug from the Company Name (e.g., "Acme Corp" -> `acme-corp`).
- **FR-003**: System MUST support storage and editing of the following fields: Name, Website URLs (multiple), HQ Location, Description, Industry (normalized).
- **FR-004**: System MUST maintain a complete revision history for all changes to Company data (creation and updates).
- **FR-005**: System MUST allow users to view the revision history (list of past versions).
- **FR-006**: System MUST allow users to revert the Company state to any previous revision.
- **FR-007**: System MUST automatically categorize companies with minimal data (e.g., only Name/Slug) as "Stubs".
- **FR-008**: The Data Model MUST strictly separate public Company information from private user metadata.
- **FR-009**: System MUST support searching/lookup of companies by Slug.
- **FR-010**: System MUST support associating multiple "Official" users with a Company, with roles: Admin, Editor, Read Only.

### Key Entities *(include if feature involves data)*

- **Company**: Public profile. Attributes: Name, Slug, HQ Location, Description, Is_Stub.
- **Industry**: Normalized category. Attributes: Name, Slug.
- **CompanyWebsite**: Official URLs. Attributes: URL, Label.
- **CompanyUser**: Official members. Attributes: User, Role.
- **CompanyRevision**: Snapshot history. Attributes: Timestamp, Snapshot Data.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new company profile with valid data in under 1 minute.
- **SC-002**: 100% of edits to Company profiles are preserved in the revision history.
- **SC-003**: System can generate a JSON/CSV dump of all Company profiles that contains ZERO private user identifiers.
- **SC-004**: Pages load successfully using the generated slugs.
