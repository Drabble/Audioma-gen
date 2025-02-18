import nltk

from ai_google import generateAudioAndSrt_google
from ai_openai import generate_thumbnail_no_text_prompt_openai
from s3 import *
from db import *
from ai_claude import *
from utils import *
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
categories = ["SCIENCE",
              "TRAVEL_CULTURE",
              "HISTORY",
              "FOOD",
              "CINEMA",
              "BELIEFS_PHILOSOPHY",
              "FANTASY",
              "NATURE",
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
        split_text = remove_empty_lines(split_text)
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
        text = remove_empty_lines(text)
        print(f"Generated intro text: {text}")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this intro text? (yes/no) or press Enter to generate a new one: ").strip().lower()

        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return text
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

def choose_thumbnail_no_text(title: str, description, filename):
    while True:
        # Generate a single phrase
        prompt = generate_thumbnail_no_text_prompt_openai(title, description)
        print(f"Using prompt: {prompt}")
        output = generate_thumbnail(prompt)
        # image_data = b64decode(b64)
        with open(DATA_DIR_GENERATED / filename, "wb") as file:
            file.write(output.read())
        # with open(DATA_DIR_GENERATED / thumbnail_filename, mode="wb") as png:
        #    png.write(image_data)
        path = DATA_DIR_GENERATED / filename
        print(f"Generated file: {path}")
        os.startfile(DATA_DIR_GENERATED / filename, "open")

        # Prompt the user to keep or reject the phrase
        choice = input(
            "Do you want to keep this thumbnail? (yes/no) or press Enter to generate a new one: ").strip().lower()
        if choice == "yes" or choice == "y":
            # User wants to keep the phrase
            return filename
        print("Generating a new thumbnail...")

def choose_book_translation(text, language):
    while True:
        translated = generate_book_translation(text, language)
        translated = remove_empty_lines(translated)
        print(translated)
        print(f"Generated book translation text for language {language}")
        return translated

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
    text = choose_book_text(idea)
    intro = choose_intro_text(idea, text)
    title = choose_title(idea, text)
    description = choose_description(idea, text)
    thumbnail = "thumbnail.webp"
    choose_thumbnail_no_text(title, description, thumbnail)
    book = Book(
        status=Status.PUBLISHED,
        isPaid=True,
        category=Category[category],
        thumbnail=thumbnail
    )
    session.add(book)
    session.commit()

    try_upload_to_s3(thumbnail, f"{book.id}/{thumbnail}")

    mp3 = "en.mp3"
    srt = "en.srt"
    duration = generateAudioAndSrt_google(
        text, "EN", mp3,
        srt)
    try_upload_to_s3(mp3, f"{book.id}/{mp3}")
    try_upload_to_s3(srt, f"{book.id}/{srt}")
    translation = Translation(
        language=Language["EN"],
        title=title,
        description=description,
        intro=intro,
        text=text,
        mp3=mp3,
        srt=srt,
        bookId=book.id,
        duration=duration,
    )
    session.add(translation)
    session.commit()

    # ----------------------- UPLOAD EACH LANGUAGE
    for key, language in languages.items():
        create_translation(book, translation, key, language)

def create_translation(book: Book, translation_en, key, language):
    print("Generating translation", key, language)
    text = choose_book_translation(translation_en.text, language)
    intro = choose_text_translation(translation_en.intro, language)
    title = choose_text_translation(translation_en.title, language)
    description = choose_text_translation(translation_en.description, language)

    mp3 = f"{key.lower()}.mp3"
    srt = f"{key.lower()}.srt"
    duration = generateAudioAndSrt_google(text, key, mp3, srt)
    try_upload_to_s3(mp3, f"{book.id}/{mp3}")
    try_upload_to_s3(srt, f"{book.id}/{srt}")

    translation = Translation(
        language=Language[key],
        title=title,
        description=description,
        intro=intro,
        text=text,
        mp3=mp3,
        srt=srt,
        bookId=book.id,
        duration=duration
    )
    session.add(translation)
    session.commit()

if __name__ == "__main__":
    main()
