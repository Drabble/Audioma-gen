import io
import os
import base64
from time import sleep, time
import requests
from pathlib import Path
from datetime import timedelta
from pydub import AudioSegment
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
    "FR": {"languageCode": "fr-FR", "name": "fr-FR-Journey-D"},
    "DE": {"languageCode": "de-DE", "name": "de-DE-Journey-D"},
    "ES": {"languageCode": "es-ES", "name": "es-ES-Wavenet-B"},
    "PT": {"languageCode": "pt-PT", "name": "pt-PT-Wavenet-C"},
    "JA": {"languageCode": "ja-JP", "name": "ja-JP-Neural2-C"},
    "IT": {"languageCode": "it-IT", "name": "it-IT-Wavenet-B"},
    "RU": {"languageCode": "ru-RU", "name": "ru-RU-Wavenet-B"},
    "KO": {"languageCode": "ko-KR", "name": "ko-KR-Wavenet-B"},
    "NL": {"languageCode": "nl-NL", "name": "nl-NL-Wavenet-A"},
    "PL": {"languageCode": "pl-PL", "name": "pl-PL-Wavenet-A"},
    "SV": {"languageCode": "sv-SE", "name": "sv-SE-Wavenet-A"},
    "TR": {"languageCode": "tr-TR", "name": "tr-TR-Wavenet-B"},
    "ZH": {"languageCode": "zh-CN", "name": "cmn-CN-Wavenet-B"},
    "HI": {"languageCode": "hi-IN", "name": "hi-IN-Wavenet-B"},
}

# Helper function to format timestamp
def format_timestamp(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    milliseconds = int((timedelta_obj.total_seconds() - total_seconds) * 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Function to get audio duration in seconds
def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_mp3(file_path)
    return audio.duration_seconds

# Function to synthesize speech, save audio, and generate SRT
def synthesize(text, lang: str, output_filename="output.mp3"):
    i = 0
    while i < 10:
        lang_config = languages[lang]

        # Payload for TTS
        payload = {
            "input": {"text": text},
            "voice": {"languageCode": lang_config["languageCode"], "name": lang_config["name"]},
            "audioConfig": {
                "audioEncoding": "LINEAR16"
            }
        }

        # Call TTS API
        response = requests.post(f"{GOOGLE_TTS_URL}?key={GOOGLE_API_KEY}", json=payload)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            sleep(2)
            i += 1
            continue

        # Decode the audio content
        audio_content = base64.b64decode(response.json()["audioContent"])

        # Load audio content into an AudioSegment object
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_content))

        # Create 600ms of silence and append it
        combined_segment = audio_segment + AudioSegment.silent(duration=600)

        # Save the combined audio directly to a file
        output_path = DATA_DIR_GENERATED / output_filename
        combined_segment.export(output_path, format="mp3", bitrate="64")
        print(f"Audio content written to {output_path}")
        return combined_segment

# Function to generate audio and SRT from input text
def generateAudioAndSrt_google(input_text, lang: str, output_audio="output.mp3", output_srt="output.srt"):
    total_audio_path = DATA_DIR_GENERATED / output_audio
    srt_path = DATA_DIR_GENERATED / output_srt

    # Initialize variables
    start_time = 0

    input_lines = input_text.splitlines()
    combined_audio = AudioSegment.empty()
    srt = ""

    for idx, line in enumerate(input_lines):
        start_synthesize_time = time()
        segment_filename = f"segment_{idx}.mp3"
        segment = synthesize(line, lang, segment_filename)
        combined_audio += segment
        end_time = combined_audio.duration_seconds

        # Add SRT entry
        start_timedelta = timedelta(seconds=start_time)
        end_timedelta = timedelta(seconds=end_time)
        srt = srt + f"{idx + 1}\n{format_timestamp(start_timedelta)} --> {format_timestamp(end_timedelta)}\n{line}\n\n"

        # Update start_time
        start_time = end_time

        synthesize_duration = time() - start_synthesize_time
        sleep_time = max(0.0, 2.1 - synthesize_duration)
        sleep(sleep_time) # JourneyRequestsPerMinutePerProject	30
    combined_audio.export(total_audio_path, format="mp3", bitrate="64")
    with open(srt_path, "a", encoding="utf-8") as srt_file:
        srt_file.write(srt)
    print(f"SRT file written to {srt_path}")
    print(f"Combined audio written to {total_audio_path}")
    duration = get_audio_duration_in_seconds(total_audio_path)
    return duration

if __name__ == "__main__":
    # Example usage
    lines = """Hello lauranne, my name is tony and i speak french\nThis is the second line"""
    try:
        generateAudioAndSrt_google(lines, "EN", "hello_world.mp3", "hello_world.srt")
    except ValueError as e:
        print(e)
