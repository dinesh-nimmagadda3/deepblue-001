# Restaurant Menu & AI Assistant (Streamlit + Groq)

A Streamlit app that displays a restaurant menu and provides an AI chat assistant powered by Groq. Users can ask about spice levels, portion sizes, ingredients, and get combo recommendations. The app supports streaming responses and lets you choose the Groq model from the sidebar.

## Features
- Menu browser with categories and expanders
- One-click combo recommendations per dish
- Chat interface with streaming AI responses
- Groq model selector in the sidebar
- Enter Groq API key securely in-app (session-only) or via environment variable

## Requirements
- Python 3.9+
- A Groq API key (`GROQ_API_KEY`)

## Setup
1. Create and activate a virtual environment (Windows PowerShell):
```bash
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install streamlit groq
```

3. Provide your Groq API key (choose one):
- In-app (recommended for quick start): open the app and paste your key under “API Settings” → “GROQ API Key”.
- Environment variable (persists across sessions):
```bash
setx GROQ_API_KEY "YOUR_KEY_HERE"
# For current shell only:
$env:GROQ_API_KEY="YOUR_KEY_HERE"
```

## Run
```bash
streamlit run app.py
```
Then open the sidebar:
- Paste your API key under “API Settings” (if not set via env)
- Choose a model (default options include `openai/gpt-oss-20b`, `llama-3.1-70b-versatile`, etc.)

## Usage
- Browse the menu on the left; click “Get Combos for …” to automatically ask the AI for pairing suggestions.
- Use the chat panel to ask questions about spice levels, portions, ingredients, or combos.
- Responses stream live into the UI for a smooth experience.

## Models
The app provides a small curated list in the sidebar (e.g. `openai/gpt-oss-20b`, `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`). If a model becomes unavailable, pick another from the list.

## Troubleshooting
- Import warning for `groq`: ensure your editor uses the venv interpreter (`.venv\Scripts\python.exe`).
- 400 error about a decommissioned model: select a different model from the sidebar.
- Missing API key warning: enter it in the sidebar or set `GROQ_API_KEY`.

## Project structure
```
.
├─ app.py           # Streamlit app
├─ .venv/           # Virtual environment (local)
└─ README.md
```

## Future enhancements
- I will be adding more features in the future.

## License
This project is provided as-is; you may adapt it to your needs.
