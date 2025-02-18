import time
import os
from pydub import AudioSegment
from pathlib import Path
from cartesia import Cartesia

from ai_prompts import *

client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))
DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

languages = {
    "EN": {
        "id": "c45bc5ec-dc68-4feb-8829-6e6b2748095d",
        "model": "sonic-english",
        "language": "en"
    },
    "FR": {
        "id": "ab7c61f5-3daa-47dd-a23b-4ac0aac5f5c3",
        "model": "sonic-multilingual",
        "language": "fr"
    },
    "DE": {
        "id": "3f6e78a8-5283-42aa-b5e7-af82e8bb310c",
        "model": "sonic-multilingual",
        "language": "de"
    },
    "ES": {
        "id": "a67e0421-22e0-4d5b-b586-bd4a64aee41d",
        "model": "sonic-multilingual",
        "language": "es"
    },
    "PT": {
        "id": "5063f45b-d9e0-4095-b056-8f3ee055d411",
        "model": "sonic-multilingual",
        "language": "pt"
    },
    "JA": {
        "id": "97e7d7a9-dfaa-4758-a936-f5f844ac34cc",
        "model": "sonic-multilingual",
        "language": "ja"
    },
    "IT": {
        "id": "029c3c7a-b6d9-44f0-814b-200d849830ff",
        "model": "sonic-multilingual",
        "language": "it"
    },
    "RU": {
        "id": "2b3bb17d-26b9-421f-b8ca-1dd92332279f",
        "model": "sonic-multilingual",
        "language": "ru"
    },
    "KO": {
        "id": "57dba6ff-fe3b-479d-836e-06f5a61cb5de",
        "model": "sonic-multilingual",
        "language": "ko"
    },
    "NL": {
        "id": "9e8db62d-056f-47f3-b3b6-1b05767f9176",
        "model": "sonic-multilingual",
        "language": "nl"
    },
    "PL": {
        "id": "4ef93bb3-682a-46e6-b881-8e157b6b4388",
        "model": "sonic-multilingual",
        "language": "PL"
    },
    "SV": {
        "id": "38a146c3-69d7-40ad-aada-76d5a2621758",
        "model": "sonic-multilingual",
        "language": "sv"
    },
    "TR": {
        "id": "5a31e4fb-f823-4359-aa91-82c0ae9a991c",
        "model": "sonic-multilingual",
        "language": "tr"
    },
    "ZH": {
        "id": "eda5bbff-1ff1-4886-8ef1-4e69a77640a0",
        "model": "sonic-multilingual",
        "language": "zh"
    },
    "HI": {
        "id": "7f423809-0011-4658-ba48-a411f5e516ba",
        "model": "sonic-multilingual",
        "language": "HI"
    }
}


def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_file(DATA_DIR_GENERATED / file_path)
    return audio.duration_seconds

def generate_audio_cartesia(text: str, language: str, filename: str):
    data = client.tts.bytes(
        model_id=languages[language]["model"],
        transcript=text,
        voice_id=languages[language]["id"],  # Barbershop Man
        # You can find the supported `output_format`s at https://docs.cartesia.ai/api-reference/tts/bytes
        output_format={
            "container": "wav",
            "encoding": "pcm_s16le",
            "sample_rate": 44100,
        },
        language=languages[language]["language"],
        _experimental_voice_controls={"speed": "slow"}
    )
    with open(DATA_DIR_GENERATED / filename, "wb") as f:
        f.write(data)


#def generate_audio_and_subtitles_cartesia(text_chunks, language: str):
#    audio_files = []
#    subtitles = []
#    start_time = 0.0
#
#    for i, chunk in enumerate(text_chunks):
#        data = client.tts.bytes(
#            model_id=languages[language]["model"],
#            transcript=chunk,
#            voice_id=languages[language]["id"],  # Barbershop Man
#            # You can find the supported `output_format`s at https://docs.cartesia.ai/api-reference/tts/bytes
#            output_format={
#                "container": "wav",
#                "encoding": "pcm_s16le",
#                "sample_rate": 44100,
#            },
#            language=languages[language]["language"],
#            _experimental_voice_controls={"speed": "slowest"}
#        )
#        filename = f'audio_chunk_{i}.wav'
#        with open(DATA_DIR_GENERATED / filename, "wb") as f:
#            f.write(data)
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
#