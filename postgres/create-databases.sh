#!/bin/bash

set -euo pipefail

psql -U $POSTGRES_USER -c "CREATE DATABASE ${UNIGATE_DB};"
psql -U $POSTGRES_USER -c "CREATE DATABASE ${AUTH_DB};"
