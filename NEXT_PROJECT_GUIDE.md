# Project 2: AI Stock News Summarizer — COMPLETED

## What We Built

Upgraded the stock news agent to send fetched news headlines to an LLM (Groq/Llama) and get back a smart, human-readable summary of the market mood.

**Actual output we got:**
```
  MARKET SUMMARY (AI)
  ────────────────────────────────────────
  - Conflict: Iran escalates US attacks
  - Energy: Oil prices surge
  - Markets: Stocks fall sharply
```

---

## What We Learned (With Detailed Explanations)

### 1. LLM API Calls — Talking to AI from Code

**What:** Instead of chatting with AI in a browser (like ChatGPT), we called an AI model directly from our Python code.

**How it works:**
```
Your Python script  →  sends text over internet  →  Groq's servers (run Llama AI model)
                    ←  receives AI response       ←
```

**The code:**
```python
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))   # Connect to Groq
response = client.chat.completions.create(           # Send request
    model="llama-3.3-70b-versatile",                 # Which AI brain to use
    messages=[...]                                   # What to send
)
answer = response.choices[0].message.content         # Extract the text response
```

**Why this matters:** Every AI agent, chatbot, or AI product works this way — sending text to an LLM and getting a response back. This is the foundation.

---

### 2. System Prompts — Controlling AI Behavior

**What:** A hidden instruction that tells the AI HOW to behave. The end user never sees it.

**Our system prompt:**
```python
"You are a stock market news analyst.
Given a list of headlines, provide exactly 3 bullet points summarizing the market mood.
Rules:
- Facts only, no investment advice
- Each bullet should cover a different theme
- Keep each bullet under 20 words
- Format: '- Theme: Summary'"
```

**Why it matters:** Without a system prompt, the AI might:
- Give investment advice (dangerous, legally risky)
- Write 10 paragraphs (too long)
- Format output randomly (can't parse it)
- Add disclaimers (unnecessary noise)

The system prompt gives you **control** over the AI's output.

**How messages work (OpenAI-style format — industry standard):**
```python
messages=[
    {"role": "system", "content": "...rules..."},    # Hidden instructions (AI's personality)
    {"role": "user", "content": "...data..."},        # What you send (headlines)
]
```
Most LLM providers (Groq, OpenAI, Anthropic) use this same format.

---

### 3. Prompt Engineering — Getting Reliable Output

**What:** The skill of writing prompts that get consistent, useful results from an AI.

**We tested 3 different system prompts on the SAME headlines:**

| Prompt Style | System Prompt | Output |
|---|---|---|
| **Expert analyst** | "You are a stock market news analyst..." | `- Conflict: Iran escalates US attacks` |
| **Beginner-friendly** | "Explain like the reader knows nothing about stocks..." | `- War: Countries fighting raises oil prices` |
| **JSON structured** | "Return a JSON array with theme, summary, sentiment..." | `{"theme": "War", "summary": "...", "sentiment": "negative"}` |

**Key lesson:** Same model + same data + different prompt = completely different output. The prompt is your main control lever.

**Structured Output (JSON) — Why it's important:**
```python
# Plain text — hard for code to work with
"Oil prices are rising due to Middle East tensions"

# JSON — easy for code to parse and use
{"theme": "Energy", "summary": "Oil rising on supply fears", "sentiment": "negative"}
```
In real AI apps, you almost always want JSON so your code can make decisions based on the AI's output (e.g., "if sentiment is negative, send an alert").

---

### 4. Temperature — Controlling Randomness

| Temperature | Behavior | Use When |
|------------|----------|----------|
| 0.0 | Same input = same output every time | News summaries, data extraction |
| 0.5 | Slight variation each time | General conversation |
| 1.0 | Very creative, different each time | Creative writing, brainstorming |

We used **0.0** because we want factual, consistent summaries — not creative stories.

---

### 5. Chaining — The Foundation of AI Agents

**What:** Output of one step becomes input of the next step.

```
Step 1: Finnhub API  →  returns 10 headlines
                              |
Step 2: Collect headlines into one string
                              |
Step 3: Send string to Groq LLM  →  returns 3-bullet summary
                              |
Step 4: Display summary in terminal
```

**Why this matters:** Every AI agent works on this principle:
- RAG: Fetch documents → Find relevant chunks → Send to LLM → Answer
- Tool-using agent: User asks question → Agent decides which tool → Runs tool → Sends result to LLM → Answer
- Multi-agent: Agent 1 output → Agent 2 input → Agent 3 input → Final result

You just built your first chain!

---

### 6. Model Comparison — Choosing the Right Brain

We compared two models on the same task:

| Model | Size | Output Quality | Speed |
|---|---|---|---|
| `llama-3.3-70b-versatile` | 70 billion parameters | Follows instructions precisely | Slower |
| `llama-3.1-8b-instant` | 8 billion parameters | Good but less precise | Faster |

**Real-world lesson:** Always start with the cheapest/smallest model. Only upgrade if quality isn't good enough. Companies waste money using expensive models when cheap ones work fine.

---

### 7. Error Handling — Building Reliable Apps

**What:** Using `try/except` to catch errors so your app doesn't crash.

**Before (crashes):**
```python
def summarize_news(headlines):
    client = Groq(api_key="wrong_key")
    response = client.chat.completions.create(...)  # CRASH! Script stops.
    return response.choices[0].message.content
```

**After (handles gracefully):**
```python
def summarize_news(headlines):
    try:
        client = Groq(api_key="wrong_key")
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate summary: {e}"  # Shows error, keeps running
```

**We tested this:** Put a wrong API key → script showed "Could not generate summary: Invalid API Key" but **didn't crash**. News still displayed, just without the AI summary.

---

### 8. Tokens & Pricing — What API Calls Cost

**What are tokens?** Chunks of text (roughly 4 characters = 1 token).

```
"Stock market rallied today" = ~5 tokens
```

- **Input tokens:** What you send (headlines) — cheaper
- **Output tokens:** What the LLM generates (summary) — more expensive

**Cost comparison:**

| Provider | Model | Cost | Our usage |
|---|---|---|---|
| Groq | Llama 3.3 70B | Free (rate-limited) | What we used |
| Google Gemini | gemini-2.0-flash | Free tier (didn't work for us) | Tried first |
| Anthropic | Claude Haiku | ~$0.003 per 1K tokens | ~₹420 ($5) for weeks |
| OpenAI | GPT-4o-mini | ~$0.003 per 1K tokens | ~₹420 ($5) for weeks |

**Tip:** Send only headlines, not full articles, to save tokens and cost.

---

## What We Tried That Didn't Work (And Why)

### Google Gemini — Free Tier Not Available

We first tried Google Gemini (free), but got this error:
```
google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED
quota exceeded... limit: 0
```

**What happened:** Gemini's free tier wasn't available for our Google account/region (India). The `limit: 0` meant zero free requests allowed.

**Lesson learned:** Free tiers vary by region and account. Always have a backup plan. We switched to **Groq** which worked immediately.

### Why Groq Worked
- Truly free with generous limits
- No credit card required
- Runs open-source models (Llama) — same quality
- Uses the same OpenAI-style API format (industry standard)

---

## Git History (3 Commits)

```
1. 5f861bc - Initial commit: stock news agent with Finnhub API
2. 10a0c19 - Add AI-powered market summary using Groq LLM
3. 1cf570f - Add error handling for LLM API calls
```

**GitHub repo:** https://github.com/Radhika3333/stock-news-agent

---

## Final Project Structure

```
stock-news-agent/
├── .env                  # FINNHUB_API_KEY + GROQ_API_KEY
├── .gitignore            # venv/, .env, __pycache__/
├── stock_news.py         # Fetch news + AI summary + error handling + 10-min loop
├── venv/                 # Python virtual environment
├── PROJECT_GUIDE.md      # Documentation for Project 1 (news fetcher)
└── NEXT_PROJECT_GUIDE.md # This file (Project 2 — AI summarizer)
```

---

## Concepts Mapped to Roadmap (balajichippada.com/roadmap)

| Roadmap Phase | Concept | Where We Used It |
|---|---|---|
| Phase 1 | Python, APIs, .env | stock_news.py (Finnhub API) |
| Phase 3 | LLM API calls | Groq SDK, client.chat.completions.create() |
| Phase 3 | System prompts | Controlled AI output format and rules |
| Phase 3 | Prompt engineering | Tested 3 different prompts, got structured JSON |
| Phase 3 | Tokens & pricing | Chose free model (Groq) over paid (Anthropic) |
| Phase 3 | Streaming (not done yet) | Future improvement |
| Foundation | Chaining | Fetch → Summarize → Display |
| Foundation | Error handling | try/except for graceful failures |

---

## Key Takeaways

1. **LLM API calls** are simple — just send text, get text back
2. **System prompts** are your main control lever — they determine output quality
3. **Same data + different prompt = completely different output** — this is prompt engineering
4. **JSON output** lets your code act on AI responses (not just display them)
5. **Error handling** makes the difference between a demo and a real app
6. **Start with the cheapest model** — upgrade only if needed
7. **Chaining** (output of step 1 → input of step 2) is the foundation of all AI agents

---

## Next Project: Document Q&A with RAG (Phase 4)

**Status:** Setup started, packages being installed in `~/Projects/doc-qa-agent/`

**What it does:** Give it documents (PDFs, text files), ask questions, get answers from YOUR data.

**New concepts:**
- Embeddings (converting text to numbers)
- Vector databases (ChromaDB)
- Chunking (splitting documents into searchable pieces)
- Semantic search (finding text by meaning, not just keywords)

**Packages needed:**
```bash
pip install chromadb sentence-transformers groq python-dotenv
```

---

## Resources

- Groq Console: https://console.groq.com/
- Groq API docs: https://console.groq.com/docs/
- Agentic AI Roadmap: https://balajichippada.com/roadmap
- Anthropic API docs: https://docs.anthropic.com/
- OpenAI API docs: https://platform.openai.com/docs
- Prompt engineering guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
