import requests
from bs4 import BeautifulSoup

def link_send():

    BASE_URL = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/?currency=UAH&page='
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    link_list = []

    response = requests.get(BASE_URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    apartments = soup.find_all('div', class_='css-1sw7q4x')

    for apartment in apartments:
            link_element = apartment.find('a', class_='css-z3gu2d', href=True)
            link = 'https://www.olx.ua'+link_element['href'] if link_element else 'Посилання не знайдено'


            link_list.append({
            'link': link
            })

    return link_list[0]
