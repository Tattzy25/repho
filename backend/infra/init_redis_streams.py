"""
Initialize Redis Streams for the orchestrated pipeline.
"""
# Install redis module by running 'pip install redis' in your terminal
import os
import redis

# Use the Redis protocol URL, not the REST URL/token.
# Example (Upstash): UPSTASH_REDIS_URL=rediss://:password@host:port
redis_url = os.getenv("UPSTASH_REDIS_URL")
if redis_url is None:
    raise RuntimeError(
        "UPSTASH_REDIS_URL is not set. Use the Redis URL (rediss://...) from Upstash, not the REST URL/token."
    )

r = redis.Redis.from_url(redis_url, decode_responses=True)

streams = ["manifest", "verify", "scaffold", "fix", "phase_complete", "phase_error"]

for stream in streams:
    try:
        # Create an empty consumer group to ensure stream exists
        r.xgroup_create(stream, "workers", id="$", mkstream=True)
        print(f"Stream '{stream}' and group 'workers' ready.")
    except redis.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"Group already exists on '{stream}'.")
        else:
            raise
