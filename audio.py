from ai_cartesia import generate_audio_cartesia
from afa_mfa import align_text_audio, textgrid_to_srt
from ai_openai import *

current_time = time.time_ns() // 1_000_000

def combine_audio_files(audio_files, output_file='combined_audio.mp3'):
    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=gap_duration_ms)

    for i, file in enumerate(audio_files):
        audio = AudioSegment.from_file(DATA_DIR_GENERATED / file)
        combined += audio

        # Add silence after each file except the last one
        if i < len(audio_files) - 1:
            combined += silence

    combined.export(DATA_DIR_GENERATED / output_file, format="mp3")


# def save_subtitles(subtitles, subtitle_file='subtitles.srt'):
#     with open(DATA_DIR_GENERATED / subtitle_file, 'w', encoding='utf-8') as f:
#         for i, (start_time, end_time, text) in enumerate(subtitles):
#             f.write(f"{i + 1}\n")
#             f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
#             f.write({text.replace("\n", " ")})
#             f.write(f"\n\n")


def convert_wav_to_mp3(wav_file, output_filename, bitrate="128k"):
    """
    Converts a WAV file to an MP3 file.

    :param wav_file: Path to the input WAV file.
    :param output_filename: The output MP3 file path.
    """
    audio = AudioSegment.from_wav(DATA_DIR_GENERATED / wav_file)
    audio.export(DATA_DIR_GENERATED / output_filename, format="mp3", bitrate=bitrate)

def convert_mp3_to_wav(mp3_file, output_filename):
    """
    Converts a WAV file to an MP3 file.

    :param mp3_file: Path to the input MP3 file.
    :param output_filename: The output WAV file path.
    """
    audio = AudioSegment.from_mp3(DATA_DIR_GENERATED / mp3_file)
    audio = audio.set_frame_rate(16000)
    audio.export(DATA_DIR_GENERATED / output_filename, format="wav")

def text_to_files(text, category, part, language):
    # text_chunks = chunk_text(text)
    filename = f"{category}_{part}_{language}_{current_time}"
    txt_filename = f"{filename}.txt"
    with open(DATA_DIR_GENERATED / txt_filename, 'w', encoding='utf-8') as f:
        f.write(text)
    wav_filename = f"{filename}.wav"
    mp3_filename = f"{filename}.mp3"
    generate_audio_cartesia(text, language, wav_filename)
    srt_filename = f"{filename}.srt"
    textgrid_filename = f"{filename}.TextGrid"
    srt_word_filename = f"{filename}_word.srt"
    convert_wav_to_mp3(wav_filename, mp3_filename)
    #convert_mp3_to_wav(mp3_filename, wav_filename)
    align_text_audio(DATA_DIR_GENERATED / txt_filename, DATA_DIR_GENERATED / wav_filename, language, DATA_DIR_GENERATED / textgrid_filename)
    textgrid_to_srt(DATA_DIR_GENERATED / textgrid_filename, DATA_DIR_GENERATED / txt_filename, DATA_DIR_GENERATED / srt_filename, DATA_DIR_GENERATED / srt_word_filename)
    # save_subtitles(subtitles, srt_filename)
    duration = get_audio_duration_in_seconds(mp3_filename)
    return mp3_filename, wav_filename, srt_filename, duration
