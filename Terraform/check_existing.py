#!/usr/bin/env python3
import json
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = os.environ.get("PANOS_HOSTNAME", "")
api_key = os.environ.get("PANOS_API_KEY", "")
version = os.environ.get("PANOS_VERSION", "v11.1")

existing = []
if host and api_key:
    url = f"https://{host}/restapi/{version}/Objects/Addresses"
    resp = requests.get(
        url,
        params={"location": "shared"},
        headers={"X-PAN-KEY": api_key},
        verify=False,
        timeout=30,
    )
    if resp.ok:
        entries = resp.json().get("result", {}).get("entry", [])
        if isinstance(entries, dict):
            entries = [entries]
        existing = [e["@name"] for e in entries if "@name" in e]

print(json.dumps({"existing_names": ",".join(existing)}))
