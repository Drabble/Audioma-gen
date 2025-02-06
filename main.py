from base64 import b64decode
import time
from pathlib import Path
from dotenv import load_dotenv
import os
import nltk

from ai_google import generateAudioAndSrt_google
from s3 import *
from db import *
from ai_claude import *
from utils import *
from audio import *
from ai_replicate import *

# Download the necessary NLTK data files
nltk.download('punkt')
nltk.download('punkt_tab')

DATA_DIR_GENERATED = Path.cwd() / "generated"
DATA_DIR_GENERATED.mkdir(exist_ok=True)

# Load environment variables from .env file located five folders up
load_dotenv()

# Set your OpenAI API key
S3_API_URL = os.getenv('S3_API_URL')
S3_API_ACCESS_KEY_ID = os.getenv('S3_API_ACCESS_KEY_ID')
S3_API_ACCESS_KEY_SECRET = os.getenv('S3_API_ACCESS_KEY_SECRET')
POSTGRES_URL = os.getenv('POSTGRES_URL')

current_time = time.time_ns() // 1_000_000

# Set of audiobook categories
bucket_name = "audioma"
categories = ["SCIENCE",
              "GEOGRAPHY",
              "HISTORY",
              "MOVIE",
              "TECHNOLOGY",
              "PHILOSOPHY",
              "FANTASY",
              "NATURE",
              # "LITERATURE",
              "PERSONAL_DEVELOPMENT",
              "ART",
              "MUSIC",
              "HEALTH"]
languages = {"FR": "French",
             "DE": "German",
             "ES": "Spanish",
             "PT": "Portuguese",
             "JA": "Japanese",
             "IT": "Italian",
             "RU": "Russian",
             # "KO": "Korean",
             # "NL": "Dutch",
             # "PL": "Polish",
             # "SV": "Swedish",
             # "TR": "Turkish",
             # "ZH": "Mandarin",
             # "HI": "Hindi"

             # "CN": "Mandarin Chinese",
             # "AR": "Arabic",
             # "NL": "Dutch",
             # "HI": "Hindi",
             # "KO": "Korean",
             # "NO": "Norwedgian",
             # "SV": "Swedish",
             # "DA": "Danish",
             # "PL": "Polish",
             # "TR": "Turkish",
             # "VI": "Vietnamese",
             # "UK": "Ukrainian",
             # "EL": "Greek"
             }


def choose_category():
    while True:
        print("Select an audiobook category:")
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        # Prompt the user to select a phrase or regenerate
        selection = input("Enter the number of the category you want to select, or press Enter to regenerate: ")

        if selection.isdigit():
            selected_index = int(selection.strip()) - 1
            if 0 <= selected_index < len(categories):
                return categories[selected_index]  # Return the selected phrase
            else:
                print("Number out of range. Please choose a number from the list.")
        print("Choosing another category...")


def choose_idea(category, used_ideas):
    # Ask if the user wants to enter an idea
    user_input_choice = input("Do you want to enter your own idea? (y/n): ").strip().lower()

    # If user wants to enter their own idea, prompt them
    if user_input_choice == 'y':
        return input("Enter your idea: ")
    while True:
        # Generate and display the list of phrases
        used_ideas_str = ', '.join(used_ideas)
        custom_idea = input("Propose an idea or leave empty:")
        ideas = generate_ideas(custom_idea, category=category, used_ideas=used_ideas_str).split("\n")
        print(f"Here are the generated ideas for the subject while avoiding used ideas {used_ideas_str}:")
        for index, idea in enumerate(ideas, start=1):
            print(f"{index}. {idea}")

        # Prompt the user to select a phrase or regenerate
        selection = input("Enter the number of the idea you want to select, or press Enter to regenerate: ")

        if selection.isdigit():
            selected_index = int(selection.strip()) - 1
            if 0 <= selected_index < len(ideas):
                return ideas[selected_index]  # Return the selected phrase
            else:
                print("Number out of range. Please choose a number from the list.")
        print("Generating a new idea...")


def choose_book_text(subject):
    while True:
        # Generate a single phrase
        text = generate_book_text(subject)
        split_text = generate_text_split(text)
        print(f"Generated book text: {split_text}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this book text? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return split_text
        print("Generating a new book...")


def choose_intro_text(subject, book_text):
    while True:
        # Generate a single phrase
        text = generate_intro_text(subject, book_text)
        split_text = generate_text_split(text)
        print(f"Generated intro text: {split_text}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this intro text? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return split_text
        print("Generating a new intro...")


def choose_title(subject, book_text):
    while True:
        # Generate a single phrase
        text = generate_title(subject, book_text)
        print(f"Generated title: {text}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this title? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return text
        print("Generating a new title...")


def choose_description(subject, book_text):
    while True:
        # Generate a single phrase
        text = generate_description(subject, book_text)
        print(f"Generated description: {text}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this description? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return text
        print("Generating a new description...")


def choose_thumbnail(title: str):
    while True:
        # Generate a single phrase
        prompt = generate_thumbnail_prompt(title)
        output = generate_thumbnail(prompt)
        # image_data = b64decode(b64)
        thumbnail_filename = f"thumbnail_{current_time}.webp"
        with open(DATA_DIR_GENERATED / thumbnail_filename, "wb") as file:
            file.write(output.read())
        # with open(DATA_DIR_GENERATED / thumbnail_filename, mode="wb") as png:
        #    png.write(image_data)
        path = DATA_DIR_GENERATED / thumbnail_filename
        print(f"Generated file: {path}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this thumbnail? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return thumbnail_filename
        print("Generating a new thumbnail...")


def choose_book_translation(text, language):
    while True:
        # Generate a single phrase
        text = generate_book_translation(text, language)
        print(f"Generated book translation text for language {language}: {text}")
        return text

        # Prompt the user to keep or reject the phrase
        # choice = input(
        #    "Do you want to keep this book text? (yes/no) or press Enter to generate a new one: ").strip().lower()


#
# if choice == "yes" or choice == "y":
#    # User wants to keep the phrase
#    return text
# print("Generating a new translation...")


def choose_text_translation(text, language):
    while True:
        # Generate a single phrase
        text = generate_text_translation(text, language)
        print(f"Generated text translation for language {language}: {text}")
        return text

        # Prompt the user to keep or reject the phrase
        # choice = input(
        #    "Do you want to keep this book text? (yes/no) or press Enter to generate a new one: ").strip().lower()

        # if choice == "yes" or choice == "y":
        #    # User wants to keep the phrase
        #    return text
        # print("Generating a new translation...")


def main():
    # category_prompt = load_category_prompt(category_key)
    category = choose_category()
    used_ideas = get_book_titles_by_category(category)
    idea = choose_idea(category, used_ideas)
    book_text = choose_book_text(idea)
    intro_text = choose_intro_text(idea, book_text)
    title = choose_title(idea, book_text)
    description = choose_description(idea, book_text)
    thumbnail_filename = choose_thumbnail(title)
    try_upload_to_s3(thumbnail_filename)
    new_book = Book(
        status=Status.PUBLISHED,
        isPaid=True,
        category=Category[category],
        thumbnailUrl=f"https://pub-8f5a34efcc0f4fe1b458438a8b574ac3.r2.dev/audioma/{thumbnail_filename}"
    )
    session.add(new_book)
    session.commit()

    filename = f"{category}_{current_time}_EN"
    # intro_mp3_filename = f"{filename}_intro.mp3"
    # intro_srt_filename = f"{filename}_intro.srt"
    book_mp3_filename = f"{filename}_book.mp3"
    book_srt_filename = f"{filename}_book.srt"
    book_text = remove_empty_lines(book_text)
    intro_text = remove_empty_lines(intro_text)
    # intro_duration = generateAudioAndSrt_google(
    #    intro_text, "EN", intro_mp3_filename,
    #    intro_srt_filename)
    book_duration = generateAudioAndSrt_google(
        book_text, "EN", book_mp3_filename,
        book_srt_filename)

    # try_upload_to_s3(intro_mp3_filename)
    # try_upload_to_s3(intro_srt_filename)
    try_upload_to_s3(book_mp3_filename)
    try_upload_to_s3(book_srt_filename)
    translation = Translation(
        language=Language["EN"],
        title=title,
        description=description,
        introTranscript=intro_text,
        bookTranscript=book_text,
        bookUrl=f"https://pub-8f5a34efcc0f4fe1b458438a8b574ac3.r2.dev/audioma/{book_mp3_filename}",
        bookSrtUrl=f"https://pub-8f5a34efcc0f4fe1b458438a8b574ac3.r2.dev/audioma/{book_srt_filename}",
        bookId=new_book.id,
        bookDuration=book_duration,
    )
    session.add(translation)
    session.commit()

    # ----------------------- UPLOAD EACH LANGUAGE
    for key, language in languages.items():
        translation_book_text = choose_book_translation(book_text, language)
        translation_intro_text = choose_book_translation(intro_text, language)
        translation_title = choose_text_translation(title, language)
        translation_description = choose_text_translation(description, language)

        filename = f"{category}_{current_time}_{key}"
        # translation_intro_mp3_filename = f"{filename}_intro.mp3"
        # translation_intro_srt_filename = f"{filename}_intro.srt"
        translation_book_mp3_filename = f"{filename}_book.mp3"
        translation_book_srt_filename = f"{filename}_book.srt"
        translation_book_text = remove_empty_lines(translation_book_text)
        translation_intro_text = remove_empty_lines(translation_intro_text)
        # translation_intro_duration = generateAudioAndSrt_google(
        #    translation_intro_text, key, translation_intro_mp3_filename, translation_intro_srt_filename)
        translation_book_duration = generateAudioAndSrt_google(
            translation_book_text, key, translation_book_mp3_filename, translation_book_srt_filename)

        # try_upload_to_s3(translation_intro_mp3_filename)
        # try_upload_to_s3(translation_intro_srt_filename)
        try_upload_to_s3(translation_book_mp3_filename)
        try_upload_to_s3(translation_book_srt_filename)
        translation = Translation(
            language=Language[key],
            title=translation_title,
            description=translation_description,
            introTranscript=translation_intro_text,
            bookTranscript=translation_book_text,
            bookUrl=f"https://pub-8f5a34efcc0f4fe1b458438a8b574ac3.r2.dev/audioma/{translation_book_mp3_filename}",
            bookSrtUrl=f"https://pub-8f5a34efcc0f4fe1b458438a8b574ac3.r2.dev/audioma/{translation_book_srt_filename}",
            bookId=new_book.id,
            bookDuration=translation_book_duration
        )
        session.add(translation)
        session.commit()


if __name__ == "__main__":
    main()
