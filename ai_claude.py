import time
from pathlib import Path
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from pydub import AudioSegment

from ai_prompts import audiobook_prompt, intro_prompt, description_prompt, book_translation_prompt, \
    text_translation_prompt, thumbnail_prompt_prompt, title_prompt, text_split_prompt, ideas_prompt, json_prompt, \
    thumbnail_no_text_prompt_prompt, thumbnail_prompt

# Note: Audio generation will need a different service since Anthropic doesn't offer TTS

load_dotenv()

# Initialize constants
model = "claude-3-5-sonnet-20241022"
temperature = 0.5
DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_file(DATA_DIR_GENERATED / file_path)
    return audio.duration_seconds


def generate_ideas(custom_idea: str, category: str, used_ideas: str):
    prompt = ideas_prompt.replace(
        "<CUSTOM_IDEA>",
        f'Propose ideas that follow the following topic "{custom_idea}"' if len(custom_idea.strip()) > 0 else ''
    ).replace("<CATEGORY>", category).replace("<USEDIDEAS>", used_ideas)

    response = anthropic.messages.create(
        model=model,
        temperature=0.8,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def generate_book_text(subject):
    prompt = audiobook_prompt.replace("<SUBJECT>", subject)
    print(f"Running prompt: {prompt}")

    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def generate_intro_text(subject, audiobook_text):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": intro_prompt.replace("<TEXT>", audiobook_text)}
        ]
    )
    return response.content[0].text


def generate_text_split(text):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": text_split_prompt.replace("<TEXT>", text)}
        ]
    )
    return response.content[0].text


def generate_title(subject, audiobook_text):
    response = anthropic.messages.create(
        model=model,
        temperature=0.8,
        max_tokens=100,
        messages=[
            {"role": "user", "content": audiobook_prompt.replace("<SUBJECT>", subject)},
            {"role": "assistant", "content": audiobook_text},
            {"role": "user", "content": title_prompt}
        ]
    )
    return response.content[0].text


def generate_description(subject, audiobook_text):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=500,
        messages=[
            {"role": "user", "content": audiobook_prompt.replace("<SUBJECT>", subject)},
            {"role": "assistant", "content": audiobook_text},
            {"role": "user", "content": description_prompt}
        ]
    )
    return response.content[0].text


def generate_book_translation(text, language):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": book_translation_prompt.replace("<LANGUAGE>", language).replace("<TEXT>", text)}
        ]
    )
    return response.content[0].text


def generate_text_translation(text, language):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": text_translation_prompt.replace("<LANGUAGE>", language).replace("<TEXT>", text)}
        ]
    )
    return response.content[0].text

def generate_thumbnail_no_text_prompt(title, description) -> str:
    response = anthropic.messages.create(
        model=model,
        temperature=0.8,
        max_tokens=500,
        messages=[
            {"role": "user", "content": thumbnail_no_text_prompt_prompt.replace("<TITLE>", title).replace("<DESCRIPTION>", description)},
        ]
    )
    return response.content[0].text

def generate_thumbnail_prompt(title, description, language):
    response = anthropic.messages.create(
        model=model,
        temperature=0.8,
        max_tokens=500,
        messages=[
            {"role": "user", "content": thumbnail_prompt_prompt.replace("<TITLE>", title).replace("<DESCRIPTION>", description).replace("<LANGUAGE>", language)}
        ]
    )
    return response.content[0].text

def generate_json_translation(json, language):
    response = anthropic.messages.create(
        model=model,
        temperature=temperature,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": json_prompt.replace("<LANGUAGE>", language) + "\n\n" + json}
        ]
    )
    return response.content[0].text

