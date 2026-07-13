import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

# Terminal colors (ANSI escape codes)
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

def summarize_news(headlines):
      """Send headlines to Groq LLM and get a market summary"""

      client = Groq(api_key=os.getenv("GROQ_API_KEY"))

      response = client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          temperature=0.0,
          max_tokens=300,
          messages=[
              {
                  "role": "system",
                  "content": """You are a stock market news analyst.
  Given a list of headlines, provide exactly 3 bullet points summarizing the market
  mood.
  Rules:
  - Facts only, no investment advice
  - Each bullet should cover a different theme
  - Keep each bullet under 20 words
  - Format: "- Theme: Summary"
  """
              },
              {
                  "role": "user",
                  "content": f"Summarize these headlines:\n{headlines}"
              }
          ]
      )

      return response.choices[0].message.content
def fetch_stock_news():
    """Fetch latest stock market news from Finnhub"""

    url = "https://finnhub.io/api/v1/news"

    params = {
        "category": "general",
        "token": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"\033[91mError: API returned status {response.status_code}\033[0m")
        return

    news_list = response.json()

    # Filter: only news from the last 1 hour
    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent_news = [
        article for article in news_list
        if datetime.fromtimestamp(article["datetime"]) >= one_hour_ago
    ][:10]

    # Header
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print(f"  {GREEN}{BOLD}STOCK NEWS{RESET}  {DIM}|  Last 1 Hour  |  {now}{RESET}")
    print(f"  {DIM}{'─' * 54}{RESET}")

    if not recent_news:
        print(f"\n  {DIM}No new stock news in the last hour.{RESET}\n")
        return

    for i, article in enumerate(recent_news, 1):
        article_time = datetime.fromtimestamp(article["datetime"])
        time_ago = datetime.now() - article_time
        minutes_ago = int(time_ago.total_seconds() / 60)

        # Time label
        if minutes_ago < 60:
            time_label = f"{minutes_ago}m ago"
        else:
            time_label = f"{minutes_ago // 60}h ago"

        # Headline
        print(f"\n  {CYAN}{BOLD}{i:2d}.{RESET} {WHITE}{BOLD}{article['headline']}{RESET}")

        # Source and time
        print(f"      {DIM}{article['source']}  |  {time_label}{RESET}")

        # Summary as bullet points
        summary = article.get("summary", "")
        if summary:
            sentences = [s.strip() for s in summary.split(". ") if s.strip()]
            for sentence in sentences[:3]:
                if not sentence.endswith("."):
                    sentence += "."
                print(f"      {YELLOW}>{RESET} {sentence}")

    # Footer
    print(f"\n  {DIM}{'─' * 54}{RESET}")
    print(f"  {DIM}Showing {len(recent_news)} article(s)  |  Source: Finnhub{RESET}")
    print()

    # AI Summary                                                                 
    headlines = "\n".join([article["headline"] for article in recent_news])
    if headlines:                                                                  
        summary = summarize_news(headlines)
        print(f"  {GREEN}{BOLD}MARKET SUMMARY (AI){RESET}")                        
        print(f"  {DIM}{'─' * 40}{RESET}")                                         
        print(f"  {summary}")
        print()   

import time

# Run immediately, then repeat every 10 minutes
while True:
    # Clear the terminal for a fresh view each time
    os.system("clear")
    fetch_stock_news()
    next_refresh = datetime.now() + timedelta(minutes=10)
    print(f"  {DIM}Next refresh at {next_refresh.strftime('%H:%M:%S')}  |  Press Ctrl+C to stop{RESET}")
    time.sleep(600)  # 600 seconds = 10 minutes
