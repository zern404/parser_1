import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "Тут ссылка"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}

def get_html(url):
    """Получаем результат запроса на страницу"""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Помилка доступу до {url}: Код {response.status_code}")
        return None

def parse_products(html):
    """Парсим данные с html"""
    
    soup = BeautifulSoup(html, 'html.parser')
    product_cards = soup.find_all('div', class_='M3v0L')

    if not product_cards:
        print("Не вдалося знайти товарні картки.")
        return []

    products = []

    for card in product_cards:
        # Получаем название товара
        title_tag = card.find('div', class_='M3v0L BXDW- sMgZR')
        title = title_tag.text.strip() if title_tag else None

        # Получаем ссылку на товар
        link_tag = card.find('a', class_='_0cNvO jwtUM')
        link = link_tag['href'] if link_tag else None
        if link and not link.startswith("http"):
            link = "кусочек ссылки" + link

        # Получаем цену товара
        price_tag = card.find('span', class_='yzKb6')
        price = price_tag.text.strip() if price_tag else None

        # Получаем количество продаж
        sales_tag = card.find('div', class_='sc-16w5pn3-4')
        sales = sales_tag.text.strip() if sales_tag else None

        # Получаем количество отзывов
        review_tag = card.find('span', class_='_3Trjq ffgjE IfSYo')
        reviews = review_tag.text.strip() if review_tag else None
        
        # Пропускаем товар, если хотя бы одно поле пустое или содержит дефолтное значение
        if None in [title, link, price, reviews]:
            continue

        products.append({
            "Назва": title,
            "Посилання": link,
            "Ціна": price,
            "Кількість продажів": sales,
            "Кількість відгуків": reviews
        })

    return products

def save_to_excel(products, filename="products.xlsx"):
    """Сохраняем в файл Excel."""
    if products:
        df = pd.DataFrame(products)
        df.to_excel(filename, index=False)
        print(f"Дані успішно збережено у файл {filename}")
    else:
        print("Немає даних для збереження.")

def main():
    html = get_html(BASE_URL)
    if html:
        products = parse_products(html)
        for product in products:
            print(product)
        save_to_excel(products)


if __name__ == "__main__":
    main()