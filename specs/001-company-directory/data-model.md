# Data Model: Company Profile Directory

## Entities

### Company

Represents the public profile of a company.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key, default=uuid.uuid7 | Unique identifier (time-sorted). |
| `name` | CharField | max_length=255 | Legal or common name. |
| `slug` | SlugField | unique, db_index | URL-friendly identifier. |
| `industry` | ForeignKey | Industry, null=True, on_delete=SET_NULL | Primary industry. |
| `hq_location` | CharField | max_length=255, blank=True | City, Country. |
| `description` | TextField | blank=True | Description of the company. |
| `is_stub` | BooleanField | default=True | True if minimal info provided. |
| `created_at` | DateTimeField | auto_now_add=True | |
| `updated_at` | DateTimeField | auto_now=True | |

**Constraints**:

- `slug` must be unique.
- `name` is required.

### CompanyWebsite

Represents one of potentially multiple official URLs for a company.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key, default=uuid.uuid7 | Unique identifier. |
| `company` | ForeignKey | Company, related_name='websites' | The company. |
| `url` | URLField | | The website URL. |
| `label` | CharField | max_length=50, blank=True | e.g. "Homepage", "Careers", "Blog". |

### Industry

Normalized industry category.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key, default=uuid.uuid7 | Unique identifier. |
| `name` | CharField | max_length=100, unique=True | e.g. "Software", "Biotech". |
| `slug` | SlugField | unique | URL-friendly identifier. |

### CompanyUser

Represents an "Official" user associated with the company (e.g. employee/admin).

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key, default=uuid.uuid7 | Unique identifier. |
| `company` | ForeignKey | Company, related_name='users' | |
| `user` | ForeignKey | User, related_name='company_memberships' | |
| `role` | CharField | choices=[ADMIN, EDITOR, READ_ONLY] | Access level. |

**Constraints**:

- Unique together: `(company, user)`.

### CompanyRevision

Represents a snapshot of a company's state at a specific point in time.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | Primary Key, default=uuid.uuid7 | Unique identifier. |
| `company` | ForeignKey | Company, related_name='revisions' | The company being edited. |
| `editor` | ForeignKey | User, null=True, related_name='company_edits' | The user who made the change. |
| `created_at` | DateTimeField | auto_now_add=True | Timestamp of change. |
| `comment` | CharField | max_length=255, blank=True | Reason for change. |
| `snapshot` | JSONField | | Full copy of Company fields + Industry Name + Website URLs. |

**Logic**:

- On every save of `Company` (or its Websites), a `CompanyRevision` is created.
- `snapshot` contains flattened data: `name`, `websites` (list of strings/objects), `hq_location`, `description`, `industry` (name/string), `is_stub`.
- This ensures the history remains readable even if relation IDs change or are deleted.

## Relationships

- One `Company` has many `CompanyWebsites`.
- One `Company` has many `CompanyUsers`.
- One `Company` belongs to one `Industry`.
- One `Company` has many `CompanyRevisions`.
