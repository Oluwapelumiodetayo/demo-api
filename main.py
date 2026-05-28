import json
import sys
import time
import uuid
import secrets
import os

import boto3
import psycopg2

from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Demo API")


def log(level: str, **fields) -> None:
    sys.stdout.write(json.dumps({"level": level, **fields}) + "\n")
    sys.stdout.flush()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())

    try:
        response = await call_next(request)

        log(
            "info",
            event="request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round((time.time() - start) * 1000, 2),
            correlation_id=correlation_id,
        )

        response.headers["x-correlation-id"] = correlation_id
        return response

    except Exception as e:
        log(
            "error",
            event="request_failed",
            method=request.method,
            path=request.url.path,
            error=str(e),
            correlation_id=correlation_id,
        )
        raise


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/regions")
def regions() -> dict:
    try:
        ec2 = boto3.client("ec2", region_name="us-east-1")
        data = ec2.describe_regions()
        names = [r["RegionName"] for r in data["Regions"]]
        return {"count": len(names), "regions": names}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AWS call failed: {e}")


@app.get("/tokens")
def tokens(length: int = 32) -> dict:
    if length < 8 or length > 128:
        raise HTTPException(status_code=400, detail="length must be between 8 and 128")

    return {"token": secrets.token_urlsafe(length)}


@app.get("/db")
def db_version() -> dict:
    url = os.environ.get("DATABASE_URL")

    if not url:
        raise HTTPException(status_code=503, detail="DATABASE_URL not set")

    try:
        with psycopg2.connect(url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                row = cur.fetchone()
                return {"postgres": row[0] if row else "unknown"}

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"DB error: {e}")

