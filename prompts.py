"""Prompt templates for the four required writing-assistant tasks."""

TASKS = {
    "blog": {
        "label": "Blog writing",
        "system": "You are a helpful blog-writing assistant. Write for the audience specified by the user. Organize the draft clearly. Do not invent facts, statistics, quotations, or sources; mark missing facts as [verify].",
    },
    "email": {
        "label": "Email drafting",
        "system": "You are a professional email-writing assistant. Draft a clear, courteous email suited to the relationship and tone the user requests. Preserve the user's intent and facts. Do not invent commitments or details.",
    },
    "code": {
        "label": "Code explanation",
        "system": "You are a patient programming tutor. Explain the supplied code accurately, define technical terms briefly, and distinguish what is visible in the code from assumptions. If context is missing, say so.",
    },
    "social": {
        "label": "Social media post",
        "system": "You are a social media writing assistant. Create concise copy for the requested platform and audience. Follow length, tone, and hashtag instructions. Do not invent claims, endorsements, or events.",
    },
}

FORMATS = {
    "text": "Return plain text. Use short paragraphs and no Markdown formatting.",
    "markdown": "Return clean Markdown with a useful heading and readable formatting.",
    "json": "Return only a valid JSON object with one string field named 'content'. Do not include Markdown fences or text outside the JSON object.",
}


def build_messages(task, content, audience, tone, output_format):
    """Build system and user messages from the selected options."""
    if task not in TASKS:
        raise ValueError("Choose one of the available writing tasks.")
    if output_format not in FORMATS:
        raise ValueError("Choose plain text, Markdown, or JSON output.")
    user_message = (
        f"Audience: {audience.strip() or 'Not specified'}\n"
        f"Tone: {tone.strip() or 'Clear and natural'}\n\n"
        f"User's material or request:\n{content.strip()}\n\n"
        f"Output format: {FORMATS[output_format]}"
    )
    return TASKS[task]["system"], user_message
