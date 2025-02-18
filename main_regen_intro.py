import nltk
from main import choose_text_translation, choose_intro_text, languages
from s3 import *
from db import *
import time

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


def main():
    books = get_books()

    for book in books:
        translation_en = get_translation(book.id)

        intro = choose_intro_text(translation_en.title, translation_en.text)
        translation_en.intro = intro
        session.add(translation_en)
        session.commit()

        user_input = input(
            f"Do you want to update the intro for '{book.id}' with title '{translation_en.title}'? (y/n): ").strip().lower()

        if user_input == 'y':
            translations = get_translations(book.id)
            for translation in translations:
                if translation.language.name == "EN":
                    continue
                intro = choose_text_translation(translation_en.intro, languages[translation.language.name])
                translation.intro = intro
                session.add(translation)
                session.commit()
        else:
            print(f"Skipping thumbnail update for '{book.id}'.")

if __name__ == "__main__":
    main()
