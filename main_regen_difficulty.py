import nltk

from ai_claude import generate_difficulty
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

    for b in books:
        translation_en = get_translation(b.id)

        difficulty = generate_difficulty(translation_en.text)
        book = session.get(Book, b.id)
        book.difficulty = difficulty
        session.add(book)
        session.commit()
        print(f"Updated '{translation_en.title}'.")

if __name__ == "__main__":
    main()
