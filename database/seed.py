import json
from typing import Any

from database.models import Author, Quote
import database.connect  # excessive?


def read_json_file(file_path: str, encoding: str = 'utf-8') -> Any:
    """Read data from json-file, and return data."""
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)

    return data


def upload_authors_to_the_database(file: str) -> None:
    """Upload authors from json-file to database."""
    authors = read_json_file(file)
    [Author(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
        ).save()
        for author in authors]


def upload_quotes_to_the_database(file: str) -> None:
    """Upload quotes from json-file to database."""
    quotes = read_json_file(file)
    for quote in quotes:
        author = Author.objects(fullname=quote['author']).first()
        if author.id:
            Quote(
                tags=quote['tags'],
                author=author.id,
                quote=quote['quote']
                ).save()

        else:
            print(f'Author "{quote["author"]}" is unknown!')


if __name__ == '__main__':
    # для завантаження json файлів у хмарну базу даних:
    if not Quote.objects():
        upload_authors_to_the_database('../jsons_files/authors.json')
        upload_quotes_to_the_database('../jsons_files/quotes.json')
