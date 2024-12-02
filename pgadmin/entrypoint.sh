#!/bin/bash

set -euo pipefail

HOST=postgres-unigate

echo "{
    \"Servers\": {
        \"1\": {
            \"Name\": \"unigate\",
            \"Group\": \"Servers\",
            \"Host\": \"${HOST}\",
            \"Port\": 5432,
            \"MaintenanceDB\": \"${POSTGRES_DB}\",
            \"Username\": \"${POSTGRES_USER}\",
            \"SSLMode\": \"prefer\",
            \"PassFile\": \"/tmp/pgpassfile\"
        }
    }
}" > /tmp/servers.json && chmod 600 /tmp/servers.json

echo "${HOST}:5432:*:${POSTGRES_USER}:${POSTGRES_PASSWORD}" > /tmp/pgpassfile && chmod 600 /tmp/pgpassfile

/entrypoint.sh
