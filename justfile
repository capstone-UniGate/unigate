set dotenv-load

venv := if os_family() == "windows" { ".venv/Scripts" } else { ".venv/bin" }
python := if os_family() == "windows" { "/python.exe" } else { "/python3" }

backend_venv := "backend" / venv
backend_python := backend_venv + python

burndown_venv := "scripts/burndown" / venv
burndown_python := burndown_venv + python

frontend_venv := "frontend" / venv
frontend_python := frontend_venv + python

@_default:
    just --list

docker-up:
    docker compose up --watch --build

docker-stop:
    docker compose stop

docker-down:
    docker compose down -v

reset-database:
    docker compose exec postgres-user-testing-unigate psql -U $POSTGRES_USER -d $POSTGRES_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"
    docker compose exec postgres-user-testing-unigate psql -U $POSTGRES_USER -d $UNIGATE_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"
    docker compose exec postgres-user-testing-unigate psql -U $POSTGRES_USER -d $AUTH_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"

init-database-docker: reset-database
    docker compose exec backend-user-testing-unigate sh -c "cd alembic_unigate && alembic upgrade head"
    docker compose exec backend-user-testing-unigate sh -c "cd alembic_auth && alembic upgrade head"
    docker compose exec backend-user-testing-unigate sh -c "python3 seeders/real.py"

init-database: reset-database
    cd backend/alembic_unigate && ../../{{ backend_venv }}/alembic upgrade head
    cd backend/alembic_auth && ../../{{ backend_venv }}/alembic upgrade head

seed-real:
    {{ backend_python }} backend/seeders/real.py

seed-fake:
    {{ backend_python }} backend/seeders/fake.py

backend-deps:
    cd backend && uv sync

backend-dev: backend-deps
    {{ backend_venv }}/fastapi dev backend/unigate/main.py

backend-python FILE *ARGS: backend-deps
    {{ backend_python }} backend/{{ FILE }} {{ ARGS }}

backend-fix: backend-deps
    {{ backend_venv }}/ruff check backend --config backend/pyproject.toml
    {{ backend_venv }}/ruff format backend --config backend/pyproject.toml

backend-only-test:
    cd backend && ../{{ backend_venv }}/pytest tests/

backend-test: backend-deps init-database seed-real backend-only-test

backend-only-test-single FILE:
    cd backend && ../{{ backend_venv }}/pytest tests/routes/{{ FILE }}

backend-test-single FILE: init-database seed-real (backend-only-test-single FILE)

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

burndown-sprint2: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py --start-date 2024-12-02 --end-date 2024-12-19 --milestone eos2 --org capstone-UniGate --project-number 5

frontend-deps:
    cd frontend && pnpm install
    cd frontend && uv sync

frontend-dev: frontend-deps
    cd frontend && pnpm run dev

frontend-prod: frontend-deps
    cd frontend && pnpm run build && pnpm run preview

frontend-fix:
    cd frontend && npx prettier . --write
    cd frontend && npx eslint --fix

frontend-only-test:
    cd frontend && ../{{ frontend_venv }}/pytest tests/

frontend-test: init-database seed-real frontend-only-test

frontend-only-test-single FILE:
    cd frontend && ../{{ frontend_venv }}/pytest tests/test_cases/{{ FILE }}

frontend-test-single FILE: init-database seed-real (frontend-only-test-single FILE)

frontend-test-no-db:
    cd frontend && ../{{ frontend_venv }}/pytest tests/
