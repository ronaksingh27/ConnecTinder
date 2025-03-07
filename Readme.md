# ConnecTinder 🔗❤️

[![Repo](https://img.shields.io/badge/GitHub-ConnecTinder-blue?logo=github)](https://github.com/ronaksingh27/ConnecTinder)

**ConnecTinder** automates your LinkedIn connection requests by fetching profiles from the **"My Network"** page and sending requests using LinkedIn's internal API. Perfect for boosting your outreach — but **use it responsibly**!

---

## 📋 Features

✅ Scrapes profile data from LinkedIn's "My Network" page using **session cookies**.  
✅ Processes and validates connection payloads before sending.  
✅ Automatically sends connection requests.  
✅ Retries failed requests.  
✅ Saves all requests and payloads to `rehydration.json` for review/debugging.

---

## 📂 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ronaksingh27/ConnecTinder.git
cd ConnecTinder
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```text
requests
beautifulsoup4
python-dotenv
```

---

### 3. Configure Your Environment (Website Cookies)

Since this script interacts with LinkedIn's internal API, **you'll need to provide cookies from your active LinkedIn session**.

Create a `.env` file in the project folder:

```ini
JSESSIONID=your_jsessionid_cookie_value
LI_AT=your_li_at_cookie_value
BSCOOKIE=your_bscookie_value
BCOOKIE=your_bcookie_value
LIDC=your_lidc_value
TIMEZONE=your_timezone_value
LIAP=your_liap_value
```

---

### 🕵️‍♂️ How to Get Cookies from LinkedIn (Using Chrome)

1. Open [https://www.linkedin.com/mynetwork/](https://www.linkedin.com/mynetwork/) in **Google Chrome**.
2. Press `F12` (or `Ctrl + Shift + I`) to open **Developer Tools**.
3. Go to the **Application** tab.
4. In the left sidebar, expand **Storage > Cookies** and select `https://www.linkedin.com`.
5. Find and copy the values for these cookies:
   - `JSESSIONID`
   - `li_at`
   - `bscookie`
   - `bcookie`
   - `lidc`
   - `timezone`
   - `liap`

Paste them into your `.env` file.

---

## 🚀 Running the Script

```bash
python main.py
```

This will:

✅ Fetch profiles from "My Network".  
✅ Prepare connection payloads.  
✅ Send connection requests.  
✅ Log processed names and save requests in `rehydration.json`.

---

## ⚠️ Important Notes

- This script **uses LinkedIn’s internal APIs** — handle with care.
- Overuse can **violate LinkedIn’s Terms of Service**, leading to account restrictions or bans.
- Intended for **educational and research purposes only** — use at your own risk.

---

## 🛠️ How It Works

1. Loads cookies from `.env` for authenticated requests.
2. Scrapes the `rehydrate-data` section from `https://www.linkedin.com/mynetwork/`.
3. Parses profiles and formats connection payloads.
4. Sends requests to:
   ```
   https://www.linkedin.com/flagship-web/rsc-action/actions/server-request
   ```
5. Saves processed data to `rehydration.json`.

---

## 📄 File Overview

| File               | Purpose |
|-------------------|---------|
| `main.py`         | Core script for fetching, processing, and sending requests |
| `.env`             | Contains your LinkedIn session cookies |
| `rehydration.json` | Stores extracted profiles and request payloads |

---

## ✅ Sample Output

```text
🔄 Starting round 1
📨 Sent request to: John
✅ Response: {"success": true}

✅ Total profiles processed: 10
Requests sent to: {'John', 'Jane', ...}
```

---

## 📬 Disclaimer

This project is created for **educational purposes only**.  
It is **not affiliated with, endorsed by, or officially connected to LinkedIn** in any way.  
Use this tool at your own risk.

