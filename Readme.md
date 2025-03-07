
# ConnecTinder 🔗❤️

[![Repo](https://img.shields.io/badge/GitHub-ConnecTinder-blue?logo=github)](https://github.com/ronaksingh27/ConnecTinder)

Automate your LinkedIn networking game with **ConnecTinder** — a script that fetches profiles from LinkedIn’s "My Network" page and sends connection requests via LinkedIn’s internal API. Ideal for automating outreach and growing your professional network — but use it wisely!

---

## 📋 Features

✅ Fetches profile data directly from LinkedIn’s "My Network" page using session cookies.  
✅ Processes and validates connection payloads before sending.  
✅ Automates sending requests to LinkedIn profiles.  
✅ Implements retry logic for failed requests.  
✅ Saves all processed payloads to `rehydration.json` for transparency and debugging.

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

### 3. Configure Your Environment

Create a `.env` file in the root folder with your **LinkedIn session cookies**:

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

## 🚀 Usage

### Run the Script

```bash
python main.py
```

This will:

✅ Fetch profiles from "My Network".  
✅ Prepare connection payloads.  
✅ Send connection requests.  
✅ Log processed names and store payloads in `rehydration.json`.

---

## ⚠️ Important Notes

- This script interacts with LinkedIn’s internal endpoints — **use responsibly**.
- Excessive or improper use may **violate LinkedIn’s Terms of Service**.
- This tool is intended for **educational and research purposes only** — you are responsible for your actions.

---

## 🛠️ How It Works (Under the Hood)

1. Loads cookies from `.env` for authenticated requests.
2. Scrapes rehydration data from `https://www.linkedin.com/mynetwork/`.
3. Parses profiles and builds payloads in LinkedIn's expected format.
4. Sends requests to LinkedIn’s internal API at:  
   `https://www.linkedin.com/flagship-web/rsc-action/actions/server-request`.

---

## 📄 File Structure

| File               | Purpose |
|-------------------|---------|
| `main.py`         | Core script handling fetching, processing, and sending |
| `.env`             | Stores your LinkedIn session cookies |
| `rehydration.json` | Profiles and payloads saved for review/debugging |

---

## ✅ Sample Output

```text
🔄 Starting round 1
📨 Sent request to: John
✅ Response: {"success": true}

✅ Total unique profiles processed: 10
Requests sent to: {'John', 'Jane', ...}
```

---

## 📬 Disclaimer

This project is provided for **educational purposes only**.  
It is **not affiliated with, endorsed by, or officially connected to LinkedIn**.  
Use it at your own risk.
