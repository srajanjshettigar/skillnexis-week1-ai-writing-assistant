"""Browser-based interface for the Week 1 AI writing assistant."""
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from llm_client import generate
from prompts import FORMATS, TASKS, build_messages


load_dotenv(Path(__file__).with_name(".env"), override=True)

st.set_page_config(
    page_title="Nexis Write | AI writing studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.markdown("## ✦ Nexis Write")
    st.caption("A small writing studio powered by your chosen language model.")
    st.divider()
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    provider_name = "Google Gemini" if provider == "gemini" else "OpenAI"
    st.markdown("**Connected provider**")
    st.info(provider_name, icon=":material/bolt:")
    st.markdown("**Quick tips**")
    st.caption("Give the assistant a clear goal and include any facts it should preserve.")
    st.caption("Temperature controls how varied the wording can be.")
    st.divider()
    st.caption("Your API key stays in the local `.env` file.")

st.title("Your AI writing studio")
st.write("Turn a topic, a rough note, or a code snippet into a polished first draft.")

task_labels = {task_data["label"]: task_key for task_key, task_data in TASKS.items()}
format_labels = {"Plain text": "text", "Markdown": "markdown", "JSON": "json"}
task_guidance = {
    "blog": {
        "material_label": "What should the blog cover?",
        "placeholder": "Describe the topic, key points to include, and the approximate length.",
        "audience_label": "Who will read the blog?",
        "audience_placeholder": "e.g. first-year computer science students",
    },
    "email": {
        "material_label": "What should the email say?",
        "placeholder": "For example: Ask my supervisor for feedback on my first week and thank them for their guidance.",
        "audience_label": "Who are you writing to?",
        "audience_placeholder": "e.g. my internship supervisor",
    },
    "code": {
        "material_label": "Paste the code you want explained",
        "placeholder": "Paste a code snippet, then add any specific questions you have about it.",
        "audience_label": "Who is the explanation for?",
        "audience_placeholder": "e.g. someone new to Python",
    },
    "social": {
        "material_label": "What should the social post be about?",
        "placeholder": "Describe the idea, key details, and any points the post should mention.",
        "audience_label": "Platform and audience",
        "audience_placeholder": "e.g. LinkedIn, for AI interns and early-career developers",
    },
}

with st.container(border=True):
    st.subheader("Create a draft")
    task_label = st.selectbox("What would you like to write?", list(task_labels))
    task = task_labels[task_label]
    guidance = task_guidance[task]
    with st.form("writing_request"):
        material = st.text_area(
            guidance["material_label"],
            height=180,
            placeholder=guidance["placeholder"],
            max_chars=int(os.getenv("MAX_INPUT_CHARS", "12000")),
        )
        audience_col, tone_col = st.columns(2)
        with audience_col:
            audience = st.text_input(guidance["audience_label"], placeholder=guidance["audience_placeholder"])
        with tone_col:
            tone = st.text_input("Tone", placeholder="e.g. polite and professional")
        controls_col, format_col = st.columns([1, 1])
        with controls_col:
            temperature = st.slider(
                "Creativity (temperature)",
                min_value=0.0,
                max_value=1.0,
                value=0.4,
                step=0.1,
                help="Lower values are more predictable; higher values allow more variation.",
            )
        with format_col:
            format_label = st.selectbox("Output format", list(format_labels))
        submitted = st.form_submit_button("Generate draft", type="primary", width="stretch")

if submitted:
    if not material.strip():
        st.warning("Add a topic or some source material first.", icon=":material/edit_note:")
    else:
        output_format = format_labels[format_label]
        system_prompt, user_prompt = build_messages(task, material, audience, tone, output_format)
        with st.spinner("Writing your draft…"):
            try:
                result = generate(system_prompt, user_prompt, temperature, output_format)
            except Exception as exc:
                st.error(f"Could not get a response: {exc}", icon=":material/error:")
            else:
                st.session_state["last_result"] = result
                st.session_state["last_format"] = output_format

if st.session_state.get("last_result"):
    st.divider()
    st.subheader("Your draft")
    output_format = st.session_state.get("last_format", "text")
    result = st.session_state["last_result"]
    with st.container(border=True):
        if output_format == "markdown":
            st.markdown(result)
        elif output_format == "json":
            st.code(result, language="json")
        else:
            st.text(result)
    st.download_button(
        "Download draft",
        data=result,
        file_name=f"writing-draft.{ 'json' if output_format == 'json' else 'md' if output_format == 'markdown' else 'txt' }",
        mime="application/json" if output_format == "json" else "text/markdown" if output_format == "markdown" else "text/plain",
    )
    st.caption("Review names, facts, and details before using or sharing an AI-generated draft.")
