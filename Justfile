#!/usr/bin/env just --justfile

# Default recipe to display help information (in order of this file)
_default:
    @just --list --unsorted

# Variables

UV_RUN := "uv run"
PNPM := "pnpm"

# Install dev dependencies
install-dev: install-python-dev install-frontend-dev

# Generates a self-signed certificate for the development server
mkcert:
    @if [ ! -f /tmp/orgtorii.crt ]; then \
        mkcert -cert-file=/tmp/orgtorii.crt -key-file=/tmp/orgtorii.key localhost 127.0.0.1; \
    fi

# Link the AI folders
ai-link:
    @mkdir -p .cursor/{commands,rules} .claude/{commands,rules}
    @stow --dir=ai --target=.cursor/commands commands
    @stow --dir=ai --target=.cursor/rules rules
    @stow --dir=ai --target=.claude/commands commands
    @stow --dir=ai --target=.claude/rules rules
###############################################
## Testing related targets
###############################################

test_command := UV_RUN + " python manage.py test"
test_options := " --shuffle --parallel=auto"

# Run fast tests (excludes browser tests)
[working-directory('orgtorii')]
test-fast:
    @{{ test_command }} {{ test_options }} --exclude-tag=browser

# Run fast tests in watch mode
[working-directory('orgtorii')]
test-fast-watch:
    @rg --files -t python,html | entr {{ test_command }} {{ test_options }} --exclude-tag=browser

# Run browser tests (uses Playwright)
[working-directory('orgtorii')]
test-browser:
    @{{ test_command }} {{ test_options }} --tag=browser

# Run all tests
[working-directory('orgtorii')]
test:
    @{{ test_command }} {{ test_options }}

# Run all tests in watch mode
[working-directory('orgtorii')]
test-watch:
    @rg --files -t python -t html | entr {{ test_command }} {{ test_options }}

[working-directory('orgtorii')]
test-unit:
    @{{ UV_RUN }} pytest

[working-directory('orgtorii/tests/e2e')]
test-e2e:
    @{{ PNPM }} test

###############################################
## Django management
###############################################

manage := UV_RUN + " python manage.py"

# Shortcut to run Django management commands
[working-directory('orgtorii')]
manage +ARGS:
    @{{ manage }} {{ ARGS }}

# Run the development server with HTTPS
[working-directory('orgtorii')]
runserver: mkcert
    @{{ manage }} runserver_plus --cert-file=/tmp/orgtorii.crt --key-file=/tmp/orgtorii.key

# Runs the development server without HTTPS
runserver-no-https:
    @{{ manage }} runserver

# Run Django migrations
[working-directory('orgtorii')]
migrate:
    @{{ manage }} migrate

# Collect static files
[working-directory('orgtorii')]
collectstatic:
    @{{ manage }} collectstatic --noinput

# Create a new Django app in the correct directory
[working-directory('orgtorii')]
startapp APP_NAME:
    @mkdir -p orgtorii/{{ APP_NAME }}
    @{{ manage }} startapp --template ../app_name {{ APP_NAME }} orgtorii/{{ APP_NAME }}
    @sed -i '' 's/{{ APP_NAME }}/orgtorii\.{{ APP_NAME }}/g' orgtorii/{{ APP_NAME }}/apps.py

###############################################
## Development
###############################################

# Install python dependencies
install-python-dev:
    @uv sync
    {{ UV_RUN }} lefthook install

# Use Ansible to setup the development environment and install dependencies
setup-dev-environment: install-dev
    {{ UV_RUN }} ansible-playbook ansible/00-dev-env-setup.yaml

# Install Playwright dependencies
playwright-install:
    @{{ UV_RUN }} playwright install

# Create Django migrations
[working-directory('orgtorii')]
makemigrations:
    @{{ manage }} makemigrations

# Run the linter and formatter
format:
    @{{ UV_RUN }} ruff check --fix
    @{{ UV_RUN }} ruff format

# Create a Django superuser
[working-directory('orgtorii')]
createsuperuser *FLAGS:
    @{{ manage }} createsuperuser {{ FLAGS }}

# Remove all Django migrations
[working-directory('orgtorii')]
clean-migrations:
    @find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -type f -delete

# Reset the database
[working-directory('orgtorii')]
reset-db:
    @{{ manage }} reset_db --noinput

# Run type checking with mypy
typecheck:
    @{{ UV_RUN }} mypy orgtorii

###############################################
## Frontend
###############################################

# Install frontend dependencies
[working-directory('frontend/orgtorii')]
install-frontend-dev:
    @{{ PNPM }} install

# Build the frontend
[working-directory('frontend/orgtorii')]
build-frontend:
    @{{ PNPM }} build

# Run the frontend development server
[working-directory('frontend/orgtorii')]
dev-frontend:
    @{{ PNPM }} dev
