#!/bin/bash
set -e

SECRET=$(aws secretsmanager get-secret-value \
    --secret-id demo-api/db-password \
    --region eu-west-2 \
    --query SecretString \
    --output text)

PASSWORD=$(echo "$SECRET" | jq -r '.password')

export DATABASE_URL="postgres://dev:${PASSWORD}@db:5432/demo"

echo "DATABASE_URL loaded from Secrets Manager."

exec python -m uvicorn main:app --host 0.0.0.0 --port 8080
