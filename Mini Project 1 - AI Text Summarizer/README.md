# AI Text Summarizer

This notebook uses Gemini to make a short summary from text you provide. You can set a maximum word count. It checks for empty input and rejects text longer than 10,000 characters.

## Run it on Windows

1. Open PowerShell in the Week 1 project folder.
2. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the notebook packages:

   ```powershell
   python -m pip install -r "Mini Project 1 - AI Text Summarizer\requirements.txt"
   ```

4. Make sure the repository's `.env` file has `LLM_PROVIDER=gemini` and a valid `GEMINI_API_KEY`. Do not upload `.env` to GitHub.
5. Open the notebook:

   ```powershell
   jupyter notebook "Mini Project 1 - AI Text Summarizer\ai_text_summarizer.ipynb"
   ```

6. If Jupyter asks, choose the Python kernel from `.venv`.
7. Run the cells from top to bottom. In the interactive section, paste your text, choose the maximum summary length, and click **Summarize**.

The notebook also shows five sample summaries with manual factual checks. They are examples, not a guarantee that every new summary will be correct.
