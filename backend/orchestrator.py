"""
Orchestrator (Nexus): routes jobs through pipeline phases, enforces order, applies rules, handles errors.
"""
import os
import json
import redis
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

# Phase streams in order
PHASES = ["manifest", "verify", "scaffold", "fix"]
# Pub/Sub channel
CHANNEL_COMPLETE = "phase_complete"
CHANNEL_ERROR = "phase_error"

state = {}  # job_id -> current phase index


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
