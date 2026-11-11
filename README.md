# Palo Alto Panorama - External_Net (Public IPv4) Builder

A lightweight Python script using the Palo Alto Panorama REST API to automatically create or update **31 public IPv4 address objects** in Panorama's **Shared** location and group them into a static address group named `External_Net`.

## Why Use This?
In Palo Alto Networks firewalls, security policies and NAT rules often need to match **all public Internet destinations** without matching internal RFC1918 traffic (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). Rather than using negated rules (which can cause unintended rule-matching behavior), this script builds the exact 31 summarized CIDR blocks covering all non-RFC1918 IPv4 space.

* **Idempotent:** Safely creates missing objects or updates existing ones without deleting anything.
* **Shared Scope:** Places all objects in Panorama `shared` so every Device Group can reference `External_Net`.
* **Consistent Naming:** Uses the format `net_<network>_<prefix>b` (e.g., `net_192.169.0.0_16b`).

## Prerequisites
* Python 3.8+
* `requests` library (`pip install -r requirements.txt`)
* Panorama admin account with **REST API** and **XML API** permissions enabled

## Quick Start

### 1. Clone the Repository & Install Dependencies
```bash
git clone https://github.com
cd panorama-external-net
pip install -r requirements.txt
```

### 2. Set Environment Variables
Never hardcode your API key in the script. Export your Panorama host and API key as environment variables:

**Linux / macOS:**
```bash
export PANORAMA_HOST="192.168.1.X"
export PANORAMA_API_KEY="your_panorama_api_key"
```

**Windows (PowerShell):**
```powershell
\$env:PANORAMA_HOST="192.168.1.X"
\$env:PANORAMA_API_KEY="your_panorama_api_key"
```

### 3. Run the Script
By default, changes are staged in Panorama's **Candidate Configuration** so you can review them before committing:
```bash
python3 panorama_external_net.py
```

To automatically commit the changes to Panorama after creation:
```bash
python3 panorama_external_net.py --commit
```
*(Note: Pushing changes from Panorama down to managed Device Groups must still be performed via Panorama's **Commit and Push** menu.)*

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
