import os
import subprocess
from aeneas.tools.execute_task import ExecuteTaskCLI
from pathlib import Path

# Output directory for generated SRT
DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

language_map = {
    "en": "eng",  # English
    "de": "deu",  # German
    "es": "spa",  # Spanish
    "fr": "fra",  # French
    "it": "ita",  # Italian
    "pt": "por",  # Portuguese
    "ru": "rus",  # Russian
    "ja": "jpn",  # Japanese
    "zh": "chi",  # Chinese
    "ar": "ara",  # Arabic
    # Add more languages as needed
}
import os

def generate_srt(audio_path, transcript_path, output_dir, language="eng"):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Correct the SRT output file path
        srt_output_path = os.path.join(output_dir, "test.srt")

        # Convert the two-letter language code to the three-letter format used by aeneas
        task_language = language_map.get(language, "eng")
        print(task_language)

        # Convert paths to strings
        audio_path_str = str(audio_path)
        transcript_path_str = str(transcript_path)
        srt_output_path_str = str(srt_output_path)

        # Build the task description
        task_description = f"task_language={task_language}|os_task_file_format=srt|is_text_type=plain|silence_threshold=0.1|max_phrase_duration=10.0"

        # Execute the task
        result = subprocess.run(
            [
                "python", "-m", "aeneas.tools.execute_task", 
                audio_path_str, transcript_path_str, task_description, srt_output_path_str
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Print stdout and stderr for debugging
        print("CLI Output:\n", result.stdout)
        if result.stderr:
            print("CLI Errors:\n", result.stderr)
        
        # Check if the file was generated
        if os.path.exists(srt_output_path_str):
            return f"SRT file generated at: {srt_output_path_str}"
        else:
            return f"Error: SRT file not found at {srt_output_path_str}"

    except Exception as e:
        return f"Error during SRT generation: {e}"

if __name__ == "__main__":
    result = generate_srt(
        DATA_DIR_GENERATED / "Category.SCIENCE_book_FR_1734200375883.wav",
        DATA_DIR_GENERATED / "Category.SCIENCE_book_FR_1734200375883.txt",
        DATA_DIR_GENERATED,
        language="fr"
    )
    print(result)