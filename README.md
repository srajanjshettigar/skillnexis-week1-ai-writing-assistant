# SkillNexis Week 1 Projects

This repository has two mini projects and the Week 1 prompt assignment.

## 1. AI Writing Assistant

### Start it on Windows

1. Open PowerShell in this folder.
2. Make a virtual environment and activate it:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create your private settings file and open it:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

5. In `.env`, choose `LLM_PROVIDER=gemini` or `LLM_PROVIDER=openai`, then add that provider's key. Keep `.env` private; it is ignored by Git.
6. Start the website:

   ```powershell
   streamlit run web_app.py
   ```

7. Open the local address shown in PowerShell. Pick a writing type, enter the details, choose a tone and format, then select **Generate draft**.

To use the command-line version instead, run `python app.py` from this folder.

## 2. AI Text Summarizer

1. Keep the virtual environment active and install its extra packages:

   ```powershell
   python -m pip install -r "Mini Project 1 - AI Text Summarizer\requirements.txt"
   ```

2. Open the notebook:

   ```powershell
   jupyter notebook "Mini Project 1 - AI Text Summarizer\ai_text_summarizer.ipynb"
   ```

3. In Jupyter, choose the `.venv` Python kernel if asked.
4. Run the notebook cells from top to bottom. In the interactive section, paste text, set the maximum summary length, and click **Summarize**.

The notebook uses the Gemini settings in the repository's `.env` file. Empty input and text over 10,000 characters are rejected. Its five sample summaries have manual factual checks; this small check does not guarantee that future summaries will be accurate.

## 3. Prompt Design & Evaluation

Open `Assignment 1/answers.md` to read the explanations, prompt examples, comparisons, and evaluation notes.

## Run the writing assistant checks

From the repository folder, run:

```powershell
python -m unittest discover -s tests -v
```

These checks do not call an AI API. Review generated text for accuracy before using it.
