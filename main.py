import os
import psycopg2
import secrets
import boto3
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Demo API")


@app.get("/health")
def health() -> dict:
    """Load balancers ping this. If we return anything other than 200, they stop sending traffic."""
    return {"status": "ok"}


@app.get("/regions")
def regions() -> dict:
    """Return all AWS regions the EC2 service is available in."""
    try:
        ec2 = boto3.client("ec2", region_name="eu-west-2")
        data = ec2.describe_regions()
        names = [r["RegionName"] for r in data["Regions"]]
        return {"count": len(names), "regions": names}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AWS call failed: {e}")


@app.get("/tokens")
def tokens(length: int = 32) -> dict:
    """Generate a URL-safe random token. Great for session IDs, reset tokens, etc."""
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
