import whisper

def transcribe_to_srt(audio_file, output_srt_file="output.srt"):
    model = whisper.load_model("base")  # You can change model to 'tiny', 'small', etc.
    
    result = model.transcribe(audio_file)
    segments = result['segments']
    
    with open(output_srt_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments):
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']

            # Convert seconds to SRT time format (HH:MM:SS,MS)
            def format_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = seconds % 60
                milliseconds = int((seconds - int(seconds)) * 1000)
                return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
    
    print(f"Subtitles saved to {output_srt_file}")

def translate_audio(audio_file, languages):
    model = whisper.load_model("base")  # Change model if needed
    results = {}

    for language in languages:
        result = model.transcribe(audio_file, task='translate', language=language)
        results[language] = result['text']
    
    return results

if __name__ == "__main__":
    transcribe_to_srt("./generated/audio_chunk_0.mp3", "subtitles.srt")

if __name__ == "__main__":
    print(translate_audio("./generated/audio_chunk_0.mp3", ["french"]))
