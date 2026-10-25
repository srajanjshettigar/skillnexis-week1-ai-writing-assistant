"""Command-line AI writing assistant for the SkillNexis Week 1 mini project."""
import os
from pathlib import Path

from dotenv import load_dotenv
from llm_client import generate
from prompts import FORMATS, TASKS, build_messages


def choose(prompt, options):
    while True:
        print("\n" + prompt)
        for number, label in options.items():
            print(f"  {number}. {label}")
        answer = input("> ").strip()
        if answer in options:
            return answer
        print("Enter one of the listed numbers.")


def read_material(max_chars):
    print("\nPaste your topic, notes, or code. Finish by typing END on its own line:")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
        if sum(len(part) + 1 for part in lines) > max_chars:
            return None
    return "\n".join(lines).strip()


def main():
    load_dotenv(Path(__file__).with_name(".env"))
    tasks = {str(i + 1): key for i, key in enumerate(TASKS)}
    task_choice = choose("Choose a writing task:", {n: TASKS[k]["label"] for n, k in tasks.items()})
    task = tasks[task_choice]

    max_chars = int(os.getenv("MAX_INPUT_CHARS", "12000"))
    content = read_material(max_chars)
    if content is None:
        print(f"Input is too long. The limit is {max_chars} characters.")
        return
    if not content:
        print("No input was entered. Run the app again and provide some material.")
        return

    audience = input("Who is this for? (optional): ").strip()
    tone = input("What tone should it use? (optional): ").strip()
    try:
        temperature = float(input("Temperature from 0 to 1 (default 0.4): ").strip() or "0.4")
        if not 0 <= temperature <= 1:
            raise ValueError
    except ValueError:
        print("Temperature must be a number from 0 to 1.")
        return

    formats = {str(i + 1): key for i, key in enumerate(FORMATS)}
    output_format = formats[choose("Choose output format:", {n: key.upper() for n, key in formats.items()})]
    system_prompt, user_prompt = build_messages(task, content, audience, tone, output_format)
    try:
        result = generate(system_prompt, user_prompt, temperature, output_format)
    except Exception as exc:
        print(f"Could not get a response: {exc}")
        return

    print("\n--- Assistant response ---\n")
    print(result)
    print("\nCheck important facts against your source before using the response.")


if __name__ == "__main__":
    main()
