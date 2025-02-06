import enum
from typing import Optional

from sqlalchemy import Boolean, create_engine, Column, String, DateTime, ForeignKey, Enum, func, Float, Integer
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file located five folders up
load_dotenv()

# S3 configuration
POSTGRES_URL = os.getenv('POSTGRES_URL')

# Database setup
Base = declarative_base()


class Category(enum.Enum):
    SCIENCE = "SCIENCE"
    HISTORY = "HISTORY"
    GEOGRAPHY = "GEOGRAPHY"
    MOVIE = "MOVIE"
    DOCUMENTARY = "DOCUMENTARY"
    LITERATURE = "LITERATURE"
    TECHNOLOGY = "TECHNOLOGY"
    BIOGRAPHY = "BIOGRAPHY"
    PHILOSOPHY = "PHILOSOPHY"
    FANTASY = "FANTASY"
    NATURE = "NATURE"
    PERSONAL_DEVELOPMENT = "PERSONAL_DEVELOPMENT"
    PSYCHOLOGY = "PSYCHOLOGY"
    ART = "ART"
    MUSIC = "MUSIC"
    HEALTH = "HEALTH"


# Define Status Enum


class Status(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


# Define Language Enum


class Language(enum.Enum):
    EN = "EN"
    FR = "FR"
    ES = "ES"
    DE = "DE"
    PT = "PT"
    JA = "JA"
    IT = "IT"
    RU = "RU"
    KO = "KO"
    NL = "NL"
    PL = "PL"
    SV = "SV"
    TR = "TR"
    ZH = "ZH"
    HI = "HI"
    # CN = "CN"
    # AR = "AR"
    # NL = "NL"
    # HI = "HI"
    # KO = "KO"
    # NO = "NO"
    # SV = "SV"
    # DA = "DA"
    # PL = "PL"
    # TR = "TR"
    # VI = "VI"
    # UK = "UK"
    # EL = "EL"


class Translation(Base):
    __tablename__ = 'Translation'
    id = Column(String, primary_key=True,
                server_default=func.gen_random_uuid())
    language = Column(Enum(Language))  # Assuming `Language` enum is imported
    title = Column(String)
    description = Column(String)
    bookUrl = Column(String)
    introTranscript = Column(String)
    bookTranscript = Column(String)
    bookSrtUrl = Column(String)
    bookDuration = Column(Float)
    bookId = Column(String, ForeignKey('Book.id')
                    )


class Book(Base):
    __tablename__ = 'Book'
    id = Column(String, primary_key=True,
                server_default=func.gen_random_uuid())
    status = Column(Enum(Status))  # Assuming `Status` enum is imported
    category = Column(Enum(Category))  # Assuming `Category` enum is imported
    thumbnailUrl = Column(String)
    isPaid = Column(Boolean)
    createdAt = Column(DateTime, default=datetime.utcnow)


# Connect to the database
engine = create_engine(POSTGRES_URL)
Session = sessionmaker(bind=engine)
session = Session()


def get_book_titles_by_category(category):
    # Query to get book titles with the specified category and 'EN' translations
    results = session.query(Translation.title). \
        join(Book, Book.id == Translation.bookId). \
        filter(Book.category == Category[category], Translation.language == Language.EN). \
        all()

    # Extract titles from the results
    titles = [result.title for result in results]
    return titles


def get_books():
    # Query to get the entire book entity with the specified category and 'EN' translations
    return session.query(Book.id, Translation.title, Book.category).join(Book, Book.id == Translation.bookId).filter(
        Translation.language == Language.EN).all()


def get_translations(book_id):
    # Query to get all translations for the given book ID
    return session.query(Translation).filter(Translation.bookId == book_id).all()


def get_translation(book_id, lang='EN') -> Optional[Translation]:
    # Query to get all translations for the given book ID
    return session.query(Translation).filter(Translation.bookId == book_id,
                                             Translation.language == lang).first()


def translation_exists(book_id: str, lang: str) -> bool:
    # Query to check if a translation exists for the given book_id and lang
    return session.query(Translation).filter(
        Translation.bookId == book_id,
        Translation.language == lang
    ).first() is not None
