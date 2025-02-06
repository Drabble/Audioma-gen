import time
import openai
from openai import OpenAI
import os
from pydub import AudioSegment
from pathlib import Path

from ai_prompts import ideas_prompt, audiobook_prompt, intro_prompt, text_split_prompt, description_prompt, \
    book_translation_prompt, text_translation_prompt, thumbnail_prompt, thumbnail_prompt_prompt, title_prompt
from prompts import *

openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

completion_model = "gpt-4o"
image_model = "dall-e-3"
tts_model = "tts-1"
gap_duration_ms = 700

DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)


def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_file(DATA_DIR_GENERATED / file_path)
    return audio.duration_seconds


def generate_ideas(custom_idea: str, category: str, used_ideas: str):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": ideas_prompt.replace("<CUSTOM_IDEA>",
                                                             f'Propose ideas that follow the following topic "{custom_idea}"' if len(
                                                                 custom_idea.strip()) > 0 else '').replace("<CATEGORY>",
                                                                                                           category).replace(
                "<USEDIDEAS>", used_ideas)}
        ]
    )
    return response.choices[0].message.content


def generate_book_text(subject):
    prompt = audiobook_prompt.replace("<SUBJECT>", subject)
    print(f"Running prompt f{prompt}")
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def generate_intro_text(subject, audiobook_text):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": audiobook_prompt.replace("<SUBJECT>", subject)},
            {"role": "assistant", "content": audiobook_text},
            {"role": "user", "content": intro_prompt},
        ]
    )
    return response.choices[0].message.content


def generate_text_split(text):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_split_prompt.replace("<TEXT>", text)},
        ]
    )
    return response.choices[0].message.content


def generate_title(subject, audiobook_text):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            {"role": "user", "content": audiobook_prompt.replace("<SUBJECT>", subject)},
            {"role": "assistant", "content": audiobook_text},
            {"role": "user", "content": title_prompt},
        ]
    )
    return response.choices[0].message.content


def generate_description(subject, audiobook_text):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            {"role": "user", "content": audiobook_prompt.replace("<SUBJECT>", subject)},
            {"role": "assistant", "content": audiobook_text},
            {"role": "user", "content": description_prompt},
        ]
    )
    return response.choices[0].message.content


def generate_book_translation(text, language):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            {"role": "user",
             "content": book_translation_prompt.replace("<LANGUAGE>", language).replace("<TEXT>", text)},
        ]
    )
    return response.choices[0].message.content


def generate_text_translation(text, language):
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            {"role": "user",
             "content": text_translation_prompt.replace("<LANGUAGE>", language).replace("<TEXT>", text)},
        ]
    )
    return response.choices[0].message.content


def generate_thumbnail_openai(title, description) -> str:
    response = openai.images.generate(
        model=image_model,
        prompt=thumbnail_prompt.replace("<TITLE>", title),
        n=1,
        response_format="b64_json",
        size="1024x1024",
        style="natural"
    )
    return response.data[0].b64_json


def generate_thumbnail_prompt(title) -> str:
    response = openai.chat.completions.create(
        model=completion_model,
        messages=[
            {"role": "user", "content": thumbnail_prompt_prompt.replace("<TITLE>", title)},
        ]
    )
    return response.choices[0].message.content

def generate_audio(text, language: str, filename: str, voice="alloy", response_format="mp3"):
    response = client.audio.speech.create(
        model=tts_model,
        voice=voice,
        input=text,
        response_format=response_format
    )
    response.write_to_file(DATA_DIR_GENERATED / filename)


#def generate_audio_and_subtitles(text_chunks, language: str, voice="alloy", response_format="wav"):
#    audio_files = []
#    subtitles = []
#    start_time = 0.0
#
#    for i, chunk in enumerate(text_chunks):
#        response = client.audio.speech.create(
#            model=tts_model,
#            voice=voice,
#            input=chunk,
#            response_format=response_format
#        )
#        filename = f'audio_chunk_{i}.wav'
#        response.write_to_file(DATA_DIR_GENERATED / filename)
#
#        duration = get_audio_duration_in_seconds(filename)
#        print("Duration in seconds of audio " +
#              filename + " is " + str(duration))
#        end_time = start_time + duration + gap_duration_ms / 1000
#        subtitles.append((start_time, end_time, chunk))
#        start_time = end_time
#
#        audio_files.append(filename)
#        time.sleep(0.1)  # to avoid hitting rate limits
#
#    return audio_files, subtitles
