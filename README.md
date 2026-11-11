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

---

## Step 1: Clone the Repository & Install Dependencies
```bash
git clone https://github.com
cd panorama-external-net
pip install -r requirements.txt
```

---

## Step 2: Generate Your Panorama API Key
Never hardcode credentials or API keys inside Python scripts. First, generate your API key from Panorama using `curl`:

**Linux / macOS:**
```bash
curl -k -X POST "https://192.168.1" --data-urlencode "user=YOUR_ADMIN_USER" --data-urlencode "password=YOUR_PASSWORD"
```

**Windows (PowerShell):**
```powershell
curl.exe -k -X POST "https://192.168.1" --data-urlencode "user=YOUR_ADMIN_USER" --data-urlencode "password=YOUR_PASSWORD"
```
Copy the long string returned between `<key>` and `</key>`.

---

## Step 3: Store `PANORAMA_API_KEY` as an Environment Variable

### Option A: Temporary Session Variable (Quickest)
These variables stay in your terminal's memory until you close the window.

**Linux / macOS:**
```bash
export PANORAMA_HOST="192.168.1.X"
export PANORAMA_API_KEY="PASTE_YOUR_KEY_HERE"
```

**Windows (PowerShell):**
```powershell
\$env:PANORAMA_HOST="192.168.1.X"
\$env:PANORAMA_API_KEY="PASTE_YOUR_KEY_HERE"
```

### Option B: Permanent User Variable (Recommended for Repeated Use)

**Windows (GUI or PowerShell):**
* **Via PowerShell:** Run the command below, then **restart your terminal or IDE** so it loads the new setting:
  ```powershell
  [System.Environment]::SetEnvironmentVariable("PANORAMA_API_KEY", "PASTE_YOUR_KEY_HERE", "User")
  [System.Environment]::SetEnvironmentVariable("PANORAMA_HOST", "192.168.1.X", "User")
  ```
* **Via Windows Settings:** Search **Edit environment variables for your account** > under **User variables**, click **New...** > add `PANORAMA_API_KEY` and `PANORAMA_HOST` > click **OK** > restart your terminal.

**Linux / macOS:**
Add the `export` lines to your shell profile (`~/.bashrc` or `~/.zshrc`) and reload it:
```bash
echo 'export PANORAMA_HOST="192.168.1.X"' >> ~/.bashrc
echo 'export PANORAMA_API_KEY="PASTE_YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

*(Tip: You can verify Python detects your key anytime by running `python -c "import os; print('Key found:', bool(os.environ.get('PANORAMA_API_KEY')))"`)*

---

## Step 4: Run the Script
By default, changes are staged in Panorama's **Candidate Configuration** so you can review them in the UI before committing:
```bash
python panorama_external_net.py
```

To automatically commit the changes to Panorama after creation:
```bash
python panorama_external_net.py --commit
```
*(Note: Pushing changes from Panorama down to managed Device Groups must still be performed via Panorama's **Commit and Push** menu.)*

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
