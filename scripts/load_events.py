import json
import requests

API_URL = "http://127.0.0.1:8000/events/ingest"

events = []

with open(
    "pipeline/generated_events.jsonl",
    "r"
) as f:

    for line in f:

        events.append(
            json.loads(line)
        )

response = requests.post(
    API_URL,
    json=events
)

print(
    response.status_code
)

print(
    response.json()
)