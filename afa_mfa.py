import os
import subprocess
from textgrid import TextGrid
import pysrt

dictionary_model_mapping = {
    "FR": "french_mfa",
    "DE": "german_mfa",
    "ES": "spanish_mfa",  # Adjust to "spanish_latin_america_mfa" or "spanish_spain_mfa" if needed.
    "PT": "portuguese_mfa",  # Adjust to "portuguese_brazil_mfa" or "portuguese_portugal_mfa" if needed.
    "JA": "japanese_mfa",
    "IT": "italian_cv",
    "RU": "russian_mfa",
    "EN": "english_us_mfa",  # Assuming US English; adjust to "english_uk_mfa" or others if needed.
    "KO": "korean_mfa",
    "NL": "dutch_cv",
    "PL": "polish_mfa",
    "SV": "swedish_mfa",
    "TR": "turkish_mfa",
    "ZH": "mandarin_mfa",  # Adjust to "mandarin_china_mfa", "mandarin_taiwan_mfa", or "mandarin_erhua_mfa" if needed.
    "HI": "hindi_cv"
}

acoustic_model_mapping = {
    "FR": "french_mfa",  # French
    "DE": "german_mfa",  # German
    "ES": "spanish_mfa",  # Spanish
    "PT": "portuguese_mfa",  # Portuguese
    "JA": "japanese_mfa",  # Japanese
    "IT": "italian_cv",  # Italian
    "RU": "russian_mfa",  # Russian
    "EN": "english_mfa",  # English
    "KO": "korean_mfa",  # Korean
    "NL": "dutch_cv",  # Dutch
    "PL": "polish_mfa",  # Polish
    "SV": "swedish_mfa",  # Swedish
    "TR": "turkish_mfa",  # Turkish
    "ZH": "mandarin_mfa",  # Mandarin
    "HI": "hindi_cv"  # Hindi
}

def run_command(command):
    """Runs a shell command and raises an error if it fails."""
    result = subprocess.run(command, shell=True, capture_output=False, text=True,
    encoding='utf-8')
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}\n{result.stderr}")
    return result.stdout

def download_models(language):
    """Downloads the required dictionary and acoustic models for MFA."""
    print("Downloading models...")
    dictionary_model = dictionary_model_mapping[language]
    acoustic_model = acoustic_model_mapping[language]

    subprocess.run(f"mfa model download dictionary {dictionary_model}", shell=True, capture_output=False, text=True)
    subprocess.run(f"mfa model download acoustic {acoustic_model}", shell=True, capture_output=False, text=True)

    return dictionary_model, acoustic_model


def align_text_audio(text_path, wav_path, language, output_path):
    """Aligns text and audio using MFA and generates a TextGrid file."""
    print("Aligning text and audio...")
    dictionary_model, acoustic_model = download_models(language)
    run_command(
        f"mfa align_one --clean --no_use_threading --single_speaker --debug {wav_path} {text_path} {dictionary_model} {acoustic_model} {output_path}" # Run with --clean if error
    )

def seconds_to_subrip_time(seconds):
    """Convert seconds (float) to SubRipTime."""
    total_ms = int(seconds * 1000)
    hours = total_ms // (60 * 60 * 1000)
    minutes = (total_ms // (60 * 1000)) % 60
    seconds = (total_ms // 1000) % 60
    milliseconds = total_ms % 1000
    return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def textgrid_to_srt(textgrid_path, original_text_path, srt_path, line_srt_path):
    """Converts TextGrid to SRT and regroups lines."""
    print("Converting TextGrid to SRT...")
    tg = TextGrid.fromFile(textgrid_path)
    intervals = tg[0]  # Assume single tier

    # Word-based SRT generation
    srt_entries = []
    for i, interval in enumerate(intervals):
        if interval.mark.strip():
            start = seconds_to_subrip_time(interval.minTime)
            end = seconds_to_subrip_time(interval.maxTime)
            text = interval.mark
            srt_entries.append(pysrt.SubRipItem(index=i + 1, start=start, end=end, text=text))

    # Save word-based SRT
    srt_file = pysrt.SubRipFile(items=srt_entries)
    srt_file.save(srt_path, encoding="utf-8")
    print(f"Saved word-based SRT: {srt_path}")

    # Line-based SRT generation
    print("Converting to line-based SRT...")
    with open(original_text_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    line_srt_entries = []
    word_index = 0
    for i, line in enumerate(lines):
        words = line.split()
        if word_index >= len(srt_entries):
            break
        start = seconds_to_subrip_time(srt_entries[word_index].start.ordinal / 1000.0)
        end = seconds_to_subrip_time(
            srt_entries[min(word_index + len(words) - 1, len(srt_entries) - 1)].end.ordinal / 1000.0
        )
        line_srt_entries.append(pysrt.SubRipItem(index=i + 1, start=start, end=end, text=line))
        word_index += len(words)

    # Save line-based SRT
    line_srt_file = pysrt.SubRipFile(items=line_srt_entries)
    line_srt_file.save(line_srt_path, encoding="utf-8")
    print(f"Saved line-based SRT: {line_srt_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Align text and audio using MFA, then generate SRT files.")
    parser.add_argument("text_path", help="Path to the source text file.")
    parser.add_argument("wav_path", help="Path to the source wav file.")
    parser.add_argument("language", help="Language for MFA models (e.g., EN, FR).")
    parser.add_argument("textgrid_path", help="Path to save textgrid file.")
    parser.add_argument("word_srt_path", help="Path to save word srt.")
    parser.add_argument("srt_path", help="Path to save srt.")

    args = parser.parse_args()

    try:
        # Step 1: Align text and audio
        align_text_audio(args.text_path, args.wav_path, args.language, args.textgrid_path)

        # Step 2: Convert TextGrid to SRT
        textgrid_to_srt(args.textgrid_path, args.text_path, args.word_srt_path, args.srt_path)

        print("All done!")
    except Exception as e:
        print(f"Error: {e}")
