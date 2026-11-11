#!/usr/bin/env python3
"""
Palo Alto Panorama REST API - Shared Objects Script
Creates or updates 31 public IPv4 address objects in 'shared' and adds them 
to the static address group External_Net.
"""

import os
import requests
import urllib3

# =========================
# CONFIGURATION
# =========================
PANORAMA_IP = "192.168.1.X"  # Replace with your Panorama IP address
API_VERSION = "v11.1"
BASE_URL = f"https://{PANORAMA_IP}/restapi/{API_VERSION}"
XML_API_URL = f"https://{PANORAMA_IP}/api/"

# Best practice: Load API key from environment variable instead of hardcoding
API_KEY = os.environ.get("PANORAMA_API_KEY", "REPLACE_WITH_NEW_KEY")

LOCATION = "shared"
COMMIT_CHANGES = False
ADDRESS_GROUP_NAME = "External_Net"

# =========================
# 31 PUBLIC IPV4 NETWORKS
# =========================
NETWORKS = [
    "0.0.0.0/5",
    "8.0.0.0/7",
    "11.0.0.0/8",
    "12.0.0.0/6",
    "16.0.0.0/4",
    "32.0.0.0/3",
    "64.0.0.0/2",
    "128.0.0.0/3",
    "160.0.0.0/5",
    "168.0.0.0/6",
    "172.0.0.0/12",
    "172.32.0.0/11",
    "172.64.0.0/10",
    "172.128.0.0/9",
    "173.0.0.0/8",
    "174.0.0.0/7",
    "176.0.0.0/4",
    "192.0.0.0/9",
    "192.128.0.0/11",
    "192.160.0.0/13",
    "192.169.0.0/16",
    "192.170.0.0/15",
    "192.172.0.0/14",
    "192.176.0.0/12",
    "192.192.0.0/10",
    "193.0.0.0/8",
    "194.0.0.0/7",
    "196.0.0.0/6",
    "200.0.0.0/5",
    "208.0.0.0/4",
    "224.0.0.0/3",
]

# =========================
# SESSION
# =========================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SESSION = requests.Session()
SESSION.headers.update(
    {
        "X-PAN-KEY": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
)

# =========================
# API HELPERS
# =========================
def base_params(name):
    return {
        "name": name,
        "location": LOCATION,
    }


def build_entry(name, entry_body):
    entry = {"@name": name}
    entry.update(entry_body)
    return entry


def get_object(endpoint, name):
    url = f"{BASE_URL}/{endpoint}"
    response = SESSION.get(
        url,
        params=base_params(name),
        verify=False,
        timeout=30,
    )

    if response.status_code == 404:
        return None

    if not response.ok:
        print(f"[ERROR] GET {endpoint} - {name} | Status: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    data = response.json()
    entries = data.get("result", {}).get("entry", [])
    if isinstance(entries, dict):
        entries = [entries]

    for entry in entries:
        if entry.get("@name") == name:
            return entry

    return None


def create_object(endpoint, name, entry_body):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"entry": [build_entry(name, entry_body)]}

    response = SESSION.post(
        url,
        params=base_params(name),
        json=payload,
        verify=False,
        timeout=30,
    )

    if not response.ok:
        print(f"[ERROR] POST {endpoint} - {name} | Status: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    print(f"[CREATE] {endpoint} (shared): {name}")


def update_object(endpoint, name, entry_body):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"entry": [build_entry(name, entry_body)]}

    response = SESSION.put(
        url,
        params=base_params(name),
        json=payload,
        verify=False,
        timeout=30,
    )

    if not response.ok:
        print(f"[ERROR] PUT {endpoint} - {name} | Status: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    print(f"[UPDATE] {endpoint} (shared): {name}")


def create_or_update_address_object(name, cidr):
    endpoint = "Objects/Addresses"
    existing = get_object(endpoint, name)
    body = {
        "ip-netmask": cidr,
        "description": "Public IPv4 network object",
    }

    if existing:
        update_object(endpoint, name, body)
    else:
        create_object(endpoint, name, body)


def create_or_update_address_group(name, members):
    endpoint = "Objects/AddressGroups"
    existing = get_object(endpoint, name)
    body = {
        "static": {"member": members},
        "description": "External public IPv4 networks",
    }

    if existing:
        update_object(endpoint, name, body)
    else:
        create_object(endpoint, name, body)


def commit_panorama():
    """
    Commits candidate config to Panorama itself using the XML API.
    Note: Pushing to Device Groups requires a separate 'commit-all' call.
    """
    params = {
        "type": "commit",
        "cmd": "<commit><description>Create/update shared External_Net objects</description></commit>",
    }
    # Use a separate request without JSON headers for XML API
    headers = {"X-PAN-KEY": API_KEY}
    response = requests.post(
        XML_API_URL,
        params=params,
        headers=headers,
        verify=False,
        timeout=60,
    )

    if not response.ok:
        print(f"[ERROR] Commit failed | Status: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    print("[COMMIT] Panorama commit job submitted:")
    print(response.text)


# =========================
# NAMING & MAIN
# =========================
def object_name_for_cidr(cidr):
    network, prefix = cidr.split("/")
    return f"net_{network}_{prefix}b"


def main():
    member_names = []

    for cidr in NETWORKS:
        object_name = object_name_for_cidr(cidr)
        create_or_update_address_object(object_name, cidr)
        member_names.append(object_name)

    create_or_update_address_group(ADDRESS_GROUP_NAME, member_names)

    if COMMIT_CHANGES:
        commit_panorama()
    else:
        print("[INFO] COMMIT_CHANGES is False; candidate configuration was not committed.")

    print("[DONE] Script completed successfully.")


if __name__ == "__main__":
    main()
