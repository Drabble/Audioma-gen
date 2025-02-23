import nltk
from ai_google import generateAudioAndSrt_google
from main import choose_book_translation, choose_text_translation
from s3 import *
from db import *
import time

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
            print(book.id, language, translation_en.title)
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
