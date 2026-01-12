# URL Contracts: Company Profile Directory

## Public Views

### List Companies

- **URL**: `/companies/`
- **Method**: `GET`
- **View**: `CompanyListView`
- **Context**:
  - `companies`: Paginated list of `Company` objects.
  - `search_query`: Current search term.

### Create Company

- **URL**: `/companies/create/`
- **Method**: `GET`, `POST`
- **View**: `CompanyCreateView`
- **Form**: `CompanyForm`
- **Permissions**: Login Required (for now).
- **On Success**: Redirect to `/companies/<slug>/`

### Company Detail

- **URL**: `/companies/<slug>/`
- **Method**: `GET`
- **View**: `CompanyDetailView`
- **Context**:
  - `company`: The `Company` object.
  - `latest_revision`: The most recent `CompanyRevision`.

### Edit Company

- **URL**: `/companies/<slug>/edit/`
- **Method**: `GET`, `POST`
- **View**: `CompanyUpdateView`
- **Form**: `CompanyForm`
- **Permissions**: Login Required. Must be an Editor or Admin of the Company.
- **On Success**: Redirect to `/companies/<slug>/`

### Revision History

- **URL**: `/companies/<slug>/history/`
- **Method**: `GET`
- **View**: `CompanyHistoryView`
- **Context**:
  - `company`: The `Company` object.
  - `revisions`: List of `CompanyRevision` objects, ordered by date desc.

### Revert Revision

- **URL**: `/companies/<slug>/history/<uuid:revision_id>/revert/`
- **Method**: `POST`
- **View**: `CompanyRevertView`
- **Permissions**: Login Required. Must be an Editor or Admin of the Company.
- **On Success**: Redirect to `/companies/<slug>/`
- **Logic**: Creates a NEW revision with the data from the old revision.
