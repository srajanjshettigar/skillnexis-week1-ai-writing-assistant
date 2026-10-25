# SkillNexis Week 1 Mini Project: AI Writing Assistant

A small Python app that calls either the OpenAI or Gemini API. It includes a browser-based writing studio and a command-line interface, with prompt templates for blog writing, email drafting, code explanation, and social media posts. Both interfaces support temperature control and plain text, Markdown, or JSON output.

## Setup (Windows)

1. Install Python 3.10 or later.
2. Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

3. In `.env`, choose one provider and add its key. For OpenAI use `LLM_PROVIDER=openai` and fill `OPENAI_API_KEY`. For Gemini use `LLM_PROVIDER=gemini` and fill `GEMINI_API_KEY`. Leave the other key blank. Keep `.env` private; it is excluded from Git.
4. Start the browser version with `streamlit run web_app.py`, then open the local address shown in PowerShell (usually `http://localhost:8501`). To use the original command-line version instead, run `python app.py`.

Choose a writing task, paste the topic or source material, and finish input with a line containing `END`. Set the audience/tone, temperature from 0 to 1, and output format.

## GitHub and evaluator setup

Upload the source files, `.env.example`, `requirements.txt`, and `.github/workflows/python-checks.yml`. The `.gitignore` excludes `.env` and `.venv`, so do not force-add them. After each push or pull request, GitHub Actions runs the key-free tests for prompt templates and provider configuration. The workflow does not need or use an API key.

To run the checks locally:

```powershell
python -m unittest discover -s tests -v
```

An evaluator who wants to generate a live answer must create their own `.env` from `.env.example` and supply their own permitted API key. Never put an API key in source code, GitHub, screenshots, or chat. API usage may incur charges.

## What the parts do

- `app.py` asks for your task and settings, checks input, calls the selected provider, and displays the answer.
- `web_app.py` provides the same writing tasks in a browser interface, with a download button for the generated draft.
- `prompts.py` stores separate instructions for each writing task and each output format.
- `llm_client.py` calls the selected API and reads its key from `.env`.
- `tests/` checks prompt building and missing/invalid provider configuration without making API calls.

Temperature changes response variety; it does not guarantee accuracy. Check generated facts against your source before using them.
