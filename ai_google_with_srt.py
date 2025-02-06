import os
import base64
import requests
from enum import Enum
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

# Output directory
DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

# API settings
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_TTS_URL = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"

# Supported languages configuration
languages = {
    "EN": {"languageCode": "en-US", "name": "en-US-Journey-D"},
    "FR": {"languageCode": "fr-FR", "name": "fr-FR-Journey-B"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Wavenet-A"},
    "ES": {"languageCode": "es-ES", "name": "es-ES-Wavenet-B"},
    "PT": {"languageCode": "pt-PT", "name": "pt-PT-Wavenet-A"},
    "JA": {"languageCode": "ja-JP", "name": "ja-JP-Wavenet-C"},
    "IT": {"languageCode": "it-IT", "name": "it-IT-Wavenet-B"},
    "RU": {"languageCode": "ru-RU", "name": "ru-RU-Wavenet-A"},
    "KO": {"languageCode": "ko-KR", "name": "ko-KR-Wavenet-B"},
    "NL": {"languageCode": "nl-NL", "name": "nl-NL-Wavenet-A"},
    "PL": {"languageCode": "pl-PL", "name": "pl-PL-Wavenet-A"},
    "SV": {"languageCode": "sv-SE", "name": "sv-SE-Wavenet-A"},
    "TR": {"languageCode": "tr-TR", "name": "tr-TR-Wavenet-B"},
    "ZH": {"languageCode": "zh-CN", "name": "cmn-CN-Wavenet-B"},
    "HI": {"languageCode": "hi-IN", "name": "hi-IN-Wavenet-B"},
}

# Enum for input languages
class VoiceLanguage(Enum):
    EN = "EN"
    FR = "FR"
    DE = "DE"
    ES = "ES"
    PT = "PT"
    JA = "JA"
    IT = "IT"
    RU = "RU"
    KO = "KO"
    NL = "NL"
    PL = "PL"
    SV = "SV"
    TR = "TR"
    ZH = "ZH"
    HI = "HI"

# Function to synthesize speech, save audio, and generate SRT
def synthesize_with_srt(text, lang: VoiceLanguage, output_filename="output.mp3"):
    if lang.value not in languages:
        raise ValueError(f"Unsupported language: {lang}")

    lang_config = languages[lang.value]
    # Estimate total duration based on average reading speed (5 chars/second)
    avg_char_per_sec = 5
    duration_seconds = len(text) / avg_char_per_sec

    # Payload for TTS
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": lang_config["languageCode"], "name": lang_config["name"],"ssmlGender": "MALE"},
        "audioConfig": {
            "audioEncoding": "MP3"
        },
        "enableTimePointing": ["SSML_MARK"]
    }

    # Call TTS API
    response = requests.post(f"{GOOGLE_TTS_URL}?key={GOOGLE_API_KEY}", json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return
    else:
        print(f"Success: {response.text}")

    # Save audio
    audio_content = base64.b64decode(response.json()["audioContent"])
    output_path = DATA_DIR_GENERATED / output_filename
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_content)
    print(f"Audio content written to {output_path}")

    # Extract timestamps and generate SRT
    timepoints = response.json().get("timepoints", [])
    generate_srt(timepoints, text, duration_seconds, output_filename)

# Function to generate SRT file
def generate_srt(timepoints, text, total_duration, output_filename):
    if not timepoints:
        print("No timepoints found, skipping SRT generation.")
        return

    srt_content = []
    start_time = timedelta(seconds=0)
    for i, timepoint in enumerate(timepoints):
        word = timepoint["markName"]
        current_time = timedelta(seconds=float(timepoint["timeSeconds"]))

        # Format SRT block
        srt_content.append(f"{i + 1}")
        srt_content.append(
            f"{format_timestamp(start_time)} --> {format_timestamp(current_time)}"
        )
        srt_content.append(word)
        srt_content.append("")
        start_time = current_time

    # Write SRT file
    srt_filename = output_filename.replace(".mp3", ".srt")
    srt_path = DATA_DIR_GENERATED / srt_filename
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write("\n".join(srt_content))
    print(f"SRT content written to {srt_path}")

# Helper function to format timestamp
def format_timestamp(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    milliseconds = int((timedelta_obj.total_seconds() - total_seconds) * 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

if __name__ == "__main__":
    # Example usage
    try:
        synthesize_with_srt("Hello lauranne how are you doing? Blu blu blu hello hello", VoiceLanguage.EN, "hello_world.mp3")
    except ValueError as e:
        print(e)
