# Coralize It

## Problem Statement 
During a high-pressure incident, engineers lose critical minutes jumping between browser tabs. Information is siloed across tools:
- **Sentry** knows what broke
- **GitHub** knows who changed what code

**Coralize It** bridges this gap using [Coral's SQL runtime](https://github.com/withcoral/coral) to enable **one-command incident diagnosis**, reducing Mean Time To Resolution (MTTR) by eliminating context-switching.

---
## What It Does

**Coralize It** is an **agentic query router** (at its current stage of development, let me state very clearly xD) that translates natural language questions into templated queries across GitHub and Sentry data sources:

```
User: "Show me the latest open issue and hint on how to fix it"
     ↓
LLM (Pass 1): Routes to LatestIssueAndHint class
     ↓
Coral: SELECT * FROM github.issues WHERE state='open' LIMIT 1
     ↓
LLM (Pass 2): Synthesizes raw data into actionable insights
     ↓
UI: Displays analysis with context

Note: A fallback to LLM (Pass 1) was planned an autonoous MCP client that could generate queries from scratch for niche cases but due to the lack of any Coral MCP client library in python this has been kept as a future scope.
```
[![Coralize-it-Dashboard.png](https://i.postimg.cc/vmZ38Z3R/Coralize-it-Dashboard.png)](https://postimg.cc/FYwjDmMG)

### Capabilities

| Feature | Query Example |
|---------|---------------|
| **Commit Frequency** | "How often are we committing to this repo?" |
| **Top Contributors** | "Who are the top 5 contributors?" |
| **Issue Tracking** | "How many open vs closed issues?" |
| **CI/CD Health** | "What's the check run success rate on main?" |
| **Code Churn** | "Show me weekly additions/deletions" |
| **Deployments** | "How many deployments in the last month?" |
| **Latest Issues** | "What's the newest open issue?" (with AI hints) |

See [queries.py](app/queries.py) for a detailed walkthrough. 

### Quick Demo

Click **"Test a Mock Issue"** button on the home page to see live examples without entering real data.

---
## Quick Start

### Prerequisites
- Python 3.12+
- [Coral CLI](https://github.com/withcoral/coral)
- Google GenAI API key
- GitHub Personal Access Token

### Installation

```bash
# Clone & setup
git clone <repo>
cd coralize-it
python3 -m venv venv
source venv/bin/activate (linux Distros and MacOS)
pip install -r requirements.txt
```

### Environment Setup

```bash
# Copy example config
cp .env.example .env

# Fill in your keys:
# GEMINI_API_KEY=your_google_genai_key
```

### Coral Source Setup
```bash
coral source add --interactive github
coral source add --interactive sentry
```

### Run Locally

```bash
flask run
# Opens http://localhost:5000

```

---
## Architecture

### **6-Phase Pipeline**
[![Coralize-It-Pipeline.png](https://i.postimg.cc/W44m0YB8/Coralize-It-Pipeline.png)](https://postimg.cc/21PBDG8L)

(Generated using NanoBanana)

---
## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.1.3 + Python 3.12.3 |
| **Frontend** | Tailwind CSS (CDN) + Vanilla JavaScript |
| **LLM Provider** | Google GenAI SDK 2.6.0 |
| **Data Access** | Coral 0.3.0+96d61f7 |
| **Validation** | Pydantic 2.13.4 |

---
## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | `GET` | Home page (form + results) |
| `/` | `POST` | Submit issue, run pipeline |
| `/api/mocks` | `GET` | Fetch mock issues (JSON) |
| `/errors/*` | - | 400, 429, 500, 503 pages |

---
Developed during WeMakeDevs x Coral Hackathon 2026 (May 25–31)

Always open for suggestions and learning: mail at vermakishlaya@protonmail.com 