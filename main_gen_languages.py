import nltk

from ai_google import generateAudioAndSrt_google
from s3 import *
from db import *
from audio import *
from utils import remove_empty_lines

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

bucket_name = "audioma"
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
             }

current_time = time.time_ns() // 1_000_000


def choose_book_translation(text, language):
    while True:
        # Generate a single phrase
        text = generate_book_translation(text, language)
        print(f"Generated book translation text for language {language}: {text}")
        return text


def choose_text_translation(text, language):
    while True:
        # Generate a single phrase
        text = generate_text_translation(text, language)
        print(f"Generated text translation for language {language}: {text}")
        return text


def choose_book():
    books = get_books()

    if not books:
        print("No books found.")
        return None

    # Display the books with indices
    print("Books:")
    for index, book in enumerate(books, start=1):
        print(f"{index}. Title: {book.title}")

    # Let the user select a book
    while True:
        try:
            choice = int(input("Enter the number of the book you want to choose: "))
            if 1 <= choice <= len(books):
                selected_book = books[choice - 1]
                print(f"You selected: {selected_book.title}")
                return selected_book
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def choose_and_display_translations(book_id):
    if not book_id:
        print("No book selected.")
        return []

    # Retrieve and display translations for the selected book
    translations = get_translations(book_id)
    if not translations:
        print("No translations available for the selected book.")
        return []

    print("Translations for the selected book:")
    for translation in translations:
        print(f"""
        Language: {translation.language}
        Title: {translation.title}
        Description: {translation.description}
        Book URL: {translation.bookUrl}
        Intro Transcript: {translation.introTranscript}
        Book Transcript: {translation.bookTranscript}
        Book SRT URL: {translation.bookSrtUrl}
        Book Duration: {translation.bookDuration}
        """)


def main():
    # category_prompt = load_category_prompt(category_key)
    book = choose_book()

    translation_en = get_translation(book.id)

    for key, language in languages.items():
        if not translation_exists(book.id, key):
            translation_book_text = choose_book_translation(translation_en.bookTranscript, language)
            translation_intro_text = choose_book_translation(translation_en.introTranscript, language)
            translation_title = choose_text_translation(translation_en.title, language)
            translation_description = choose_text_translation(translation_en.description, language)
            filename = f"{book.category.name}_{current_time}_{key}"
            translation_intro_mp3_filename = f"{filename}_intro.mp3"
            translation_intro_srt_filename = f"{filename}_intro.srt"
            translation_book_mp3_filename = f"{filename}_book.mp3"
            translation_book_srt_filename = f"{filename}_book.srt"
            translation_intro_text = remove_empty_lines(translation_intro_text)
            translation_book_text = remove_empty_lines(translation_book_text)
            translation_intro_duration = generateAudioAndSrt_google(
                translation_intro_text, key, translation_intro_mp3_filename, translation_intro_srt_filename)
            translation_book_duration = generateAudioAndSrt_google(
                translation_book_text, key, translation_book_mp3_filename, translation_book_srt_filename)
            try_upload_to_s3(translation_intro_mp3_filename)
            try_upload_to_s3(translation_intro_srt_filename)
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
                bookId=book.id,
                bookDuration=translation_book_duration
            )
            session.add(translation)
            session.commit()


if __name__ == "__main__":
    main()
