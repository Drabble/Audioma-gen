import nltk

from main import choose_thumbnail_no_text
from main_regen_audio import choose_book
from s3 import *
from db import *
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


def main():
    book = choose_book()

    translation_en = get_translation(book.id)
    thumbnail = "thumbnail.webp"

    user_input = input(
        f"Do you want to update the thumbnail for '{book.id}' with title '{translation_en.title}'? (y/n): ").strip().lower()

    if user_input == 'y':
        choose_thumbnail_no_text(translation_en.title, translation_en.description, thumbnail)
        try_upload_to_s3(thumbnail, f"{book.id}/{thumbnail}")
    else:
        print(f"Skipping thumbnail update for '{book.id}'.")

if __name__ == "__main__":
    main()
