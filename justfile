set dotenv-load


venv := if os_family() == "windows" { ".venv/Scripts" } else { ".venv/bin" }
python := if os_family() == "windows" { "/python.exe" } else { "/python3" }

backend_venv := "backend" / venv
backend_python := backend_venv + python

burndown_venv := "scripts/burndown" / venv
burndown_python := burndown_venv + python

@_default:
    just --list

backend-deps:
    cd backend && uv sync

backend-dev: backend-deps
    {{ backend_venv }}/fastapi dev backend/unigate/main.py

backend-python FILE *ARGS: backend-deps
    {{ backend_python }} backend/{{ FILE }} {{ ARGS }}

backend-fix: backend-deps
    {{ backend_venv }}/ruff check backend --config backend/pyproject.toml
    {{ backend_venv }}/ruff format backend --config backend/pyproject.toml

pre-commit: backend-deps
    {{ backend_venv }}/pre-commit run --all-files

burndown-deps:
    cd scripts/burndown && uv sync

burndown-fix: burndown-deps
    {{ burndown_venv }}/ruff check scripts/burndown --config scripts/burndown/pyproject.toml
    {{ burndown_venv }}/ruff format scripts/burndown --config scripts/burndown/pyproject.toml

burndown *ARGS: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py {{ ARGS }}

burndown-sprint1: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py --start-date 2024-11-10 --end-date 2024-11-27 --milestone eos1 --org capstone-UniGate --project-number 5

frontend-deps:
    cd frontend && pnpm install

frontend-dev: frontend-deps
    cd frontend && pnpm run dev

frontend-fix:
    cd frontend && npx prettier . --write
    cd frontend && npx eslint --fix
