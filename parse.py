import requests
from bs4 import BeautifulSoup


def parse_apartments():

    BASE_URL = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/?currency=UAH&page='
    PRICE = '&search%5Bfilter_float_price%3Ato%5D=12000'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    CITY_FILTER = 'Київ'
    DISTRICT_FILTER = ['Печерський', 'Шевченківський', 'Подільський', 'Оболонський', "Солом'янський"]

    apartments_list = []

    num_page = 25

    for page in range(1, num_page + 1):
        num = 0
        
        url = f'{BASE_URL}{page}{PRICE}'

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Ошибка при загрузке страницы {page}: {response.status_code}")
            continue  # Переход на следующую страницу, если ошибка
        print('Парсим...')
        soup = BeautifulSoup(response.content, 'html.parser')

        apartments = soup.find_all('div', class_='css-1sw7q4x')

        for apartment in apartments:
            title_element = apartment.find('h6', class_='css-1wxaaza')
            title = title_element.get_text(strip=True) if title_element is not None else 'Назва не вказана'

            price_element = apartment.find('p', class_='css-13afqrm')
            price_text = price_element.get_text(strip=True) if price_element is not None else ''

            address_element = apartment.find('p', class_='css-1mwdrlh')
            address = address_element.get_text(strip=True) if address_element is not None else 'Адреса не вказана'

            link_element = apartment.find('a', class_='css-z3gu2d', href=True)
            link = 'https://www.olx.ua'+link_element['href'] if link_element else 'Посилання не знайдено'

            parts = address.split(',')

            if len(parts) >= 2:
                city = parts[0].strip()
                district_and_date = parts[1].strip()
                district_parts = district_and_date.split('-')
                district = district_parts[0].strip()
                date = district_parts[1].strip()
            
            else:
                city = 'Пусто'
                district_and_date = 'Пусто'

            if (city == CITY_FILTER) and any(district in address for district in DISTRICT_FILTER):
                apartments_list.append({
                    'link': link
                })

    return apartments_list
                 

        


    
