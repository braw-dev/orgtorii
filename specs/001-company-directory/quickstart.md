# Quickstart: Company Profile Directory

## Prerequisites

- Local development environment running (`just install-dev`).

## Database Migrations

This feature introduces a new app `companies`.

```bash
just makemigrations
just migrate
```

## Running the Server

```bash
just runserver
```

## Accessing the Feature

1. Navigate to `http://localhost:8000/companies/`.
2. Click "Add Company" to create a new profile.
3. Fill in the form (e.g., Name: "Acme Corp").
4. Submit and view the new profile at `/companies/acme-corp/`.
5. Click "Edit" to modify details.
6. Click "History" to view the revision log.

## Testing

Run the tests for the companies app:

```bash
just test-unit orgtorii.companies
```
