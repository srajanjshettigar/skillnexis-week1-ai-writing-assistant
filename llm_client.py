"""OpenAI and Gemini adapters for text generation."""
import os


def generate(system_prompt, user_prompt, temperature, output_format):
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is empty. Add your key to the private .env file.")
        from openai import OpenAI

        request = {
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if output_format == "json":
            request["response_format"] = {"type": "json_object"}
        response = OpenAI(api_key=api_key).chat.completions.create(**request)
        return response.choices[0].message.content or ""

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is empty. Add your key to the private .env file.")
        from google import genai
        from google.genai import types

        config = {"system_instruction": system_prompt, "temperature": temperature}
        if output_format == "json":
            config["response_mime_type"] = "application/json"
        # Keep a strong reference to the client for the complete request. Some
        # SDK/httpx combinations close a temporary client's transport too early.
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
                contents=user_prompt,
                config=types.GenerateContentConfig(**config),
            )
            return response.text or ""
        finally:
            client.close()

    raise RuntimeError("LLM_PROVIDER must be 'openai' or 'gemini'.")
