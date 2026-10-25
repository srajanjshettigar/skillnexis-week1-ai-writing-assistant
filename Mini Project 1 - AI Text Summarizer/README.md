# Mini Project 1: AI Text Summarizer

Open `ai_text_summarizer.ipynb` in Jupyter and run the cells from top to bottom. The interactive cell accepts pasted text and a maximum summary word count. It rejects empty input and text over 10,000 characters before sending a request.

## Setup

From the Week 1 repository root, activate the existing virtual environment and install the notebook dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r "Mini Project 1 - AI Text Summarizer/requirements.txt"
```

The notebook uses the repository-root `.env` if present. Set `LLM_PROVIDER=gemini`, `GEMINI_API_KEY`, and `GEMINI_MODEL=gemini-3.5-flash-lite` there. The API key must remain private and is excluded by the root `.gitignore`. Alternatively, set `GEMINI_API_KEY` in the environment.

The notebook includes five actual Gemini summaries, factual-accuracy checks, the prompt, and a short explanation of the model. The evaluation is a small manual sample, not a guarantee of future accuracy.
