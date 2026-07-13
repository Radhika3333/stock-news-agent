# Next Project: AI Stock News Summarizer

## Goal

Upgrade the stock news agent to send fetched news to an LLM (Claude/GPT) and get back a smart, human-readable summary of the market mood — not just raw headlines.

**Example output:**
```
MARKET SUMMARY (Last 1 Hour):
  1. Tech stocks rallying — Nasdaq up 2% driven by chip sector gains
  2. Oil prices rising — Middle East supply concerns pushing crude higher
  3. Gold weakening — Rate-hike expectations pulling investors away from safe havens
```

---

## What You'll Learn

| Concept | Why It Matters |
|---------|---------------|
| LLM API calls (Claude/GPT) | Core skill — every AI agent talks to an LLM |
| System prompts | Control HOW the LLM responds (tone, format, rules) |
| Prompt engineering | Get reliable, structured output instead of random text |
| Tokens & pricing | Understand what API calls cost and how to optimize |
| Chaining (fetch → summarize) | Foundation of agentic AI — one step feeds the next |

---

## Prerequisites

Before starting, make sure you're comfortable with:

- [x] Python basics (functions, loops, dicts) — done in stock-news-agent
- [x] HTTP API calls with requests — done in stock-news-agent
- [x] .env files for secrets — done in stock-news-agent
- [ ] Python classes (OOP basics) — learn before or during this project
- [ ] Anthropic or OpenAI API key — sign up before starting

---

## Phase 1: Get an API Key

### Option A: Anthropic (Claude) — Recommended
1. Go to https://console.anthropic.com/
2. Sign up and add billing (small amount, $5 is enough)
3. Go to API Keys → Create new key
4. Save it in your `.env` file as `ANTHROPIC_API_KEY=your_key`

### Option B: OpenAI (GPT)
1. Go to https://platform.openai.com/
2. Sign up and add billing
3. Go to API Keys → Create new secret key
4. Save it in your `.env` file as `OPENAI_API_KEY=your_key`

### Cost Estimate
- Each summary call uses ~500-1000 tokens
- At ~$0.003 per 1K tokens (Claude Haiku / GPT-4o-mini)
- Running every 10 min = 144 calls/day = ~$0.50/day
- Use a cheap model (Haiku or GPT-4o-mini) for this project

---

## Phase 2: Install the SDK

```bash
cd ~/Projects/stock-news-agent
source venv/bin/activate

# For Anthropic (Claude)
pip install anthropic

# OR for OpenAI (GPT)
pip install openai
```

### What is an SDK?
SDK = Software Development Kit. It's a library that makes it easy to call an API.
Instead of manually building HTTP requests, you call simple Python methods like:
```python
client.messages.create(model="...", messages=[...])
```

---

## Phase 3: Understand Key Concepts

### What is a System Prompt?
A hidden instruction that tells the LLM HOW to behave. The user never sees it.

```python
# System prompt sets the rules
system = "You are a stock market analyst. Summarize news in 3 bullet points. No opinions, no advice, only facts."

# User message is the actual input
user = "Here are today's headlines: ..."
```

**Why it matters:** Without a system prompt, the LLM might give investment advice, add disclaimers, or format output randomly. The system prompt gives you control.

### What are Tokens?
Tokens are chunks of text (roughly 4 characters = 1 token). You pay per token.

```
"Stock market rallied today" = 5 tokens (approximate)
```

- **Input tokens:** What you send (headlines) — cheaper
- **Output tokens:** What the LLM generates (summary) — more expensive
- **Tip:** Send only headlines, not full articles, to save tokens

### What is Temperature?
Controls randomness in the LLM's output.

| Temperature | Behavior |
|------------|----------|
| 0.0 | Deterministic — same input gives same output every time |
| 0.5 | Balanced — slight variation |
| 1.0 | Creative — more random, different each time |

For news summaries, use **0.0 or 0.2** — you want consistent, factual output.

---

## Phase 4: Build the Summarizer

### Step 1: Create a New Function

Add a function that takes headlines and sends them to the LLM:

```python
import anthropic  # or openai

def summarize_news(headlines):
    """Send headlines to Claude and get a market summary"""

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from .env

    # System prompt: controls the LLM's behavior
    system_prompt = """You are a stock market news analyst.
    Given a list of headlines, provide exactly 3 bullet points summarizing the market mood.
    Rules:
    - Facts only, no investment advice or suggestions
    - Each bullet should cover a different theme (e.g., tech, commodities, geopolitics)
    - Keep each bullet under 20 words
    - Format: "- Theme: Summary"
    """

    # Send the headlines to Claude
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # cheap, fast model
        max_tokens=300,                      # limit output length
        temperature=0.0,                     # factual, no creativity
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Summarize these headlines:\n{headlines}"}
        ]
    )

    # Extract and return the text response
    return message.content[0].text
```

### Step 2: Connect It to Your Existing Script

After fetching news, collect headlines and pass them to the summarizer:

```python
# Collect headlines from fetched news
headlines = "\n".join([article["headline"] for article in recent_news])

# Get AI summary
if headlines:
    summary = summarize_news(headlines)
    print("\n  MARKET SUMMARY")
    print(f"  {'─' * 40}")
    print(f"  {summary}")
```

### Step 3: Test It

```bash
python3 stock_news.py
```

Expected output:
```
  STOCK NEWS (Last 1 Hour) — 2026-07-10 19:30:00
  ──────────────────────────────────────────────────────

   1. Nasdaq rallies on chip stocks...
      Reuters  |  23m ago

   2. Oil prices climb amid Middle East tensions...
      Reuters  |  45m ago

  ──────────────────────────────────────────────────────

  MARKET SUMMARY
  ────────────────────────────────────────
  - Tech: Chip sector driving Nasdaq higher, offsetting geopolitical concerns
  - Energy: Oil prices rising on Middle East supply disruption fears
  - Macro: Markets largely shrugging off US-Iran tensions, focused on earnings
```

---

## Phase 5: Experiment & Learn

Once the basic version works, try these exercises:

### Exercise 1: Change the System Prompt
Try different prompts and see how output changes:
- "Summarize like a Twitter thread"
- "Summarize for a beginner who knows nothing about stocks"
- "Respond in JSON format with keys: theme, summary, sentiment"

### Exercise 2: Structured Output (JSON)
Make the LLM return JSON instead of plain text:
```python
system_prompt = """Return a JSON array with exactly 3 objects.
Each object has: {"theme": "...", "summary": "...", "sentiment": "positive/negative/neutral"}
No markdown, no explanation, just the JSON array."""
```
Then parse it in Python with `json.loads(response)`.

### Exercise 3: Compare Models
Try different models and compare speed, quality, and cost:
- `claude-haiku-4-5-20251001` — cheapest, fastest
- `claude-sonnet-4-6` — balanced
- `gpt-4o-mini` — OpenAI's cheap option

### Exercise 4: Add Error Handling
What happens when:
- The API key is wrong?
- You hit the rate limit?
- The LLM returns unexpected format?

Add try/except blocks and handle these gracefully.

---

## Project Structure (Final)

```
stock-news-agent/
├── .env                  # FINNHUB_API_KEY + ANTHROPIC_API_KEY
├── .gitignore            # venv/, .env
├── stock_news.py         # Fetch news + AI summary + 10-min loop
├── venv/                 # Python virtual environment
├── PROJECT_GUIDE.md      # Documentation for the first project
└── NEXT_PROJECT_GUIDE.md # This file
```

---

## Key Takeaways After This Project

After completing this, you will understand:

1. **How to call an LLM from code** — not just chat UI, but programmatic access
2. **System prompts** — how to control LLM behavior reliably
3. **Prompt engineering** — getting structured, predictable output
4. **Token economics** — what API calls cost and how to optimize
5. **Chaining** — feeding output from one step (fetch) into another (summarize)

These are the building blocks for Phase 4 (RAG) and Phase 5 (Tool-using agents) in the roadmap.

---

## Resources

- Anthropic API docs: https://docs.anthropic.com/
- OpenAI API docs: https://platform.openai.com/docs
- Prompt engineering guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- Model pricing: https://www.anthropic.com/pricing (Anthropic) / https://openai.com/pricing (OpenAI)
