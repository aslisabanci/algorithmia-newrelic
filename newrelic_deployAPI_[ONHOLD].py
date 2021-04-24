import os
import requests
from datetime import datetime, timezone

API_KEY = os.getenv("API_KEY")

headers = {
    "Api-Key": "NRII-jSAFF79d1VL0WdxAhtJ6S8lIVBWLroA4",
    "Content-Type": "application/json",
}

now_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print(now_date)

data = {
    "deployment": {
        "revision": "REVISION",
        "changelog": "Added: /v2/deployments.rb, Removed: None",
        "description": "Added a deployments resource to the v2 API",
        "user": "asabanci@algorithmia.io",
        "timestamp": now_date,
    }
}

response = requests.post(
    "https://api.newrelic.com/v2/applications/$APP_ID/deployments.json",
    headers=headers,
    data=data,
)

