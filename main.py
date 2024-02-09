import requests
from bs4 import BeautifulSoup
import re
def fetch_book_info_by_isbn(isbn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    search_url = f"https://www.findbook.ru/search/d0?s=1&pvalue={isbn}&ptype=4"
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    book_info = {
        'title': None,
        'authors': None,
        'publisher': None,
        'year': None,
        'image_url': None
    }

    title_tag = soup.find('big')
    if title_tag:
        book_info['title'] = title_tag.text.strip()

    details_tag = title_tag.find_next('small') if title_tag else None
    if details_tag:
        details_text = details_tag.text.strip()

        if '(' in details_text and ')' in details_text:
            # Разбиваем текст на части для автора и издательства/года
            authors_part, publisher_year_part = details_text.split('(', 1)
            publisher_year_part = publisher_year_part.strip(')')
            publisher_info, year_info = publisher_year_part.split(',', 1)  # Разделяем издательство и год

            book_info['authors'] = authors_part.strip()
            book_info['publisher'] = publisher_info.strip()
            if year_info.strip().isdigit():
                book_info['year'] = year_info.strip()
        else:
            # Если информация представлена в иной форме, обрабатываем её как имя автора
            book_info['authors'] = details_text
    image_tag = soup.find('td', {'width': '60'}).find('img')
    if image_tag and 'src' in image_tag.attrs:
        book_info['image_url'] = image_tag['src']

    return book_info
isbn_input = input("Введите ISBN книги для поиска: ")

# Пример использования
isbn = "978-5-4335-0977-1"

book_info = fetch_book_info_by_isbn(isbn_input)

if "error" not in book_info:
    print("Найденная информация о книге:")
    print(book_info)
else:
    print(book_info["error"])