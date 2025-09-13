"""
Orchestrator (Nexus): routes jobs through pipeline phases, enforces order, applies rules, handles errors.
"""
import os
import json
import redis
import psycopg2
from dotenv import load_dotenv
from rules import RuleEngine, Manifest

load_dotenv()

# Redis connection (Upstash via Redis protocol URL)
# Example: UPSTASH_REDIS_URL=rediss://:password@host:port
redis_url = os.getenv("UPSTASH_REDIS_URL")
if redis_url is None:
    raise RuntimeError(
        "UPSTASH_REDIS_URL is not set. Use the Redis URL (rediss://...) from Upstash, not the REST URL/token."
    )
r = redis.Redis.from_url(redis_url, decode_responses=True)

# Postgres connection for error logging
db_url = os.getenv("DATABASE_URL")
conn = None
if db_url:
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS orchestrator_errors (
                    id SERIAL PRIMARY KEY,
                    job_id TEXT,
                    phase TEXT,
                    error TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
                """
            )
    except Exception as e:
        print(f"Failed to initialize Postgres logging: {e}")
        conn = None
else:
    print("DATABASE_URL is not set; errors will not be logged to Postgres")

# Phase streams in order
PHASES = ["manifest", "verify", "scaffold", "fix"]
# Pub/Sub channel
CHANNEL_COMPLETE = "phase_complete"
CHANNEL_ERROR = "phase_error"

state = {}  # job_id -> current phase index


def log_error(err: dict) -> None:
    """Persist error details to Postgres if a connection is available."""
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO orchestrator_errors (job_id, phase, error) VALUES (%s, %s, %s)",
                (err["job_id"], err["phase"], err["error"]),
            )
    except Exception as e:
        print(f"Failed to log error to Postgres: {e}")


def handle_complete(message):
    data = json.loads(message)
    job_id = data["job_id"]
    phase = data["phase"]
    idx = PHASES.index(phase)
    print(f"Job {job_id}: completed phase '{phase}'")

    # Validate results
    try:
        if phase == "manifest":
            # load manifest file from storage
            m = Manifest.parse_file(f"jobs/{job_id}/manifest.json")
            RuleEngine.validate_manifest(m)
        elif phase == "scaffold":
            m = Manifest.parse_file(f"jobs/{job_id}/manifest.json")
            RuleEngine.validate_scaffold(f"jobs/{job_id}/scaffold", m)
        # other phases can add validations
    except Exception as e:
        err = {"job_id": job_id, "phase": phase, "error": str(e)}
        r.publish(CHANNEL_ERROR, json.dumps(err))
        log_error(err)
        print(f"Validation failed: {e}")
        return

    # Dispatch next phase
    next_idx = idx + 1
    if next_idx < len(PHASES):
        next_phase = PHASES[next_idx]
        r.xadd(next_phase, {"job_id": job_id})
    else:
        print(f"Job {job_id} complete ✅")


def orchestrate():
    pubsub = r.pubsub()
    pubsub.subscribe(**{CHANNEL_COMPLETE: lambda msg: handle_complete(msg['data'])})
    print("Orchestrator listening for phase completions...")
    pubsub.run_in_thread(sleep_time=0.01)


if __name__ == '__main__':
    orchestrate()
