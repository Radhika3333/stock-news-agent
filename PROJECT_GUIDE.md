# Stock News Agent - Project Guide

## What Is This?

A Python script that automatically fetches the latest stock market news every 10 minutes and displays it in your terminal with clean, color-coded formatting.

- News source: Finnhub API (free tier)
- Refresh interval: Every 10 minutes
- Filter: Only shows news from the last 1 hour
- Display: Top 10 articles with headline, source, time ago, and summary bullet points

---

## Project Structure

```
stock-news-agent/
├── .env                # Stores your secret Finnhub API key
├── .gitignore          # Tells git to ignore venv/ and .env
├── stock_news.py       # Main script (fetches + displays + loops)
├── venv/               # Python virtual environment (isolated packages)
└── PROJECT_GUIDE.md    # This file
```

---

## Concepts Used (What Each Thing Does)

### 1. Virtual Environment (venv)

**What:** An isolated Python environment inside the `venv/` folder.

**Why:** Without it, packages install globally and can conflict with other projects. Each project gets its own clean set of packages.

**Commands:**
```bash
python3 -m venv venv          # Create it (one time)
source venv/bin/activate       # Activate it (every time you open terminal)
deactivate                     # Deactivate when done
```

### 2. pip (Package Manager)

**What:** Python's package installer — like an app store for Python libraries.

**Why:** To install third-party libraries that aren't built into Python.

**Packages we installed:**
| Package | Purpose |
|---------|---------|
| `requests` | Makes HTTP calls to Finnhub's API |
| `python-dotenv` | Reads API key from `.env` file securely |

### 3. .env File (Environment Variables)

**What:** A file that stores secret values like API keys.

**Why:** Never hardcode secrets in your code. If you push to GitHub, your key gets exposed. `.env` stays local and is listed in `.gitignore`.

**Format:**
```
FINNHUB_API_KEY=your_key_here
```

**How it's loaded in code:**
```python
from dotenv import load_dotenv
load_dotenv()                              # Reads .env file
API_KEY = os.getenv("FINNHUB_API_KEY")     # Gets the value
```

### 4. API (Application Programming Interface)

**What:** A way for your code to talk to Finnhub's servers over the internet.

**How it works:**
1. Your script sends an HTTP GET request to `https://finnhub.io/api/v1/news`
2. It includes your API key (for authentication) and category (general)
3. Finnhub's server responds with news data in JSON format
4. Your script parses the JSON and displays it

**In code:**
```python
response = requests.get(url, params=params)   # Send request
news_list = response.json()                    # Parse JSON response
```

### 5. JSON (JavaScript Object Notation)

**What:** A text format for structured data. The API returns news as a list of JSON objects.

**Example of one article from Finnhub:**
```json
{
  "headline": "Nasdaq ends sharply higher",
  "source": "Reuters",
  "datetime": 1752192960,
  "summary": "Nasdaq ends sharply higher; chip surge offsets Iran worries.",
  "url": "https://..."
}
```

**In Python**, this becomes a dictionary — accessed with `article["headline"]`.

### 6. ANSI Escape Codes (Terminal Colors)

**What:** Special character sequences that tell the terminal to display text in color.

**Examples used in the script:**
```python
"\033[92m"   # Green text
"\033[96m"   # Cyan text
"\033[93m"   # Yellow text
"\033[1m"    # Bold
"\033[2m"    # Dim
"\033[0m"    # Reset to normal
```

**How:** You wrap text between a color code and `\033[0m` (reset):
```python
print(f"\033[92mThis is green\033[0m and this is normal")
```

### 7. time.sleep() (The Loop)

**What:** Pauses the script for a given number of seconds.

**How the 10-minute loop works:**
```python
while True:                # Run forever
    fetch_stock_news()     # Fetch and display news
    time.sleep(600)        # Wait 600 seconds (10 minutes)
                           # Then loop back to the top
```

**Stop it:** Press `Ctrl+C` in the terminal.

### 8. datetime and timedelta (Time Filtering)

**What:** Python's built-in tools for working with dates and times.

**How we filter to last 1 hour:**
```python
one_hour_ago = datetime.now() - timedelta(hours=1)   # Current time minus 1 hour
# Keep only articles newer than one_hour_ago
recent_news = [a for a in news_list if datetime.fromtimestamp(a["datetime"]) >= one_hour_ago]
```

**Unix timestamp:** Finnhub returns time as seconds since Jan 1, 1970 (e.g., `1752192960`). `datetime.fromtimestamp()` converts this to a readable date.

---

## How to Run

```bash
# Step 1: Go to project folder
cd ~/Projects/stock-news-agent

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Run the script
python3 stock_news.py

# Step 4: Stop it
# Press Ctrl+C
```

---

## How the Script Flows

```
START
  |
  v
Load API key from .env
  |
  v
[LOOP STARTS]
  |
  v
Clear terminal screen
  |
  v
Send GET request to Finnhub API
  |
  v
Receive JSON response (list of articles)
  |
  v
Filter: keep only articles from last 1 hour
  |
  v
Take top 10 articles
  |
  v
For each article:
  - Print headline (white, bold)
  - Print source + "Xm ago" (dim gray)
  - Print summary as bullet points (yellow arrows)
  |
  v
Print footer (article count)
  |
  v
Show "Next refresh at HH:MM:SS"
  |
  v
Sleep 600 seconds (10 minutes)
  |
  v
[LOOP REPEATS]
```

---

## API Details

| Field | Value |
|-------|-------|
| Provider | Finnhub.io |
| Endpoint | `https://finnhub.io/api/v1/news` |
| Method | GET |
| Auth | API key as `token` query parameter |
| Free tier | 60 requests/minute |
| Response | JSON array of news articles |

---

## Future Improvements (Optional)

- Filter by specific stocks (e.g., AAPL, TSLA) using Finnhub's company news endpoint
- Save news to a log file for history
- Send alerts to Slack/email for breaking news
- Use cron job instead of loop for background scheduling
- Add Indian stock market news (NSE/BSE) using a different API

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'requests'` | Run `source venv/bin/activate` first, then `pip install requests python-dotenv` |
| `Error: API returned status 401` | Your API key is wrong. Check `.env` file |
| `Error: API returned status 429` | Too many requests. Wait a minute and try again |
| `No new stock news in the last hour` | Normal during off-market hours. US markets run 9:30 AM - 4 PM ET (7 PM - 1:30 AM IST) |
| Script doesn't show colors | Your terminal may not support ANSI codes. Try using VS Code's integrated terminal |
