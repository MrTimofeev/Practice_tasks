import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
import xlrd
import csv
import io


class ParserTrade():

    def __init__(self, max_pages=100, min_date=datetime(2023, 1, 1)):
        self.max_pages = max_pages
        self.min_date = min_date
        self.base_url = "https://spimex.com"
        self.all_links = []
        self.all_data = []
        self.count = 1
        self.flag = False

    def parse_links(self, max_page=100):
        while self.count <= max_page and not self.flag:
            url = f"{self.base_url}/markets/oil_products/trades/results/?page=page-{self.count}&bxajaxid=d609bce6ada86eff0b6f7e49e6bae904"

            try:
                responce = requests.get(url)
                responce.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при загрузке страницы {self.count}: {e}")
                break

            soup = BeautifulSoup(responce.text, "lxml")
            links = soup.find_all(
                'div', attrs={'class': 'accordeon-inner__item'})

            for link in links:
                a_tag = link.find(
                    "a", class_='accordeon-inner__item-title link xls')
                if not a_tag:
                    continue

                url = self.base_url + a_tag.get('href', '')

                date_span = link.find("span")

                try:
                    date_parsed = datetime.strptime(
                        date_span.text.strip(), '%d.%m.%Y')
                except ValueError:
                    print(f"Неверный формат даты: {date_span.text}")
                    continue

                if date_parsed >= self.min_date:
                    print("Эта дата подходит!")
                else:
                    print("Эта дата слишком старая.")
                    self.flag = True
                    break

                if "oil_xls" in url:
                    self.all_links.append(
                        {"url": url, "date": date_span.text.strip()})

            self.count += 1

    def save_links(self):
        with open('news.json', 'w', encoding='utf-8') as file:
            # Записываем данные в формате JSON
            json.dump(self.all_links, file, ensure_ascii=False, indent=4)

    def load_links(self):
        with open('news.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def parse_xls(self):
        data = self.load_links()
        for item in data:
            try:

                responce = requests.get(item["url"])
                xls_data = io.BytesIO(responce.content)
                book = xlrd.open_workbook(file_contents=xls_data.getvalue())
                shet = book.sheet_by_index(0)

                for row_num in range(shet.nrows):
                    cols = shet.row_values(row_num)

                    if len(cols) < 6:
                        continue

                    product_id = cols[1]
                    count = cols[-1]

                    if len(product_id) == 11 and count.isdigit():
                        self.all_data.append({
                            "exchange_product_id": product_id,
                            "exchange_product_name": cols[2],
                            "oil_id":  product_id[:4],
                            "delivery_basis_id": product_id[4:7],
                            "delivery_basis_name": cols[3],
                            "delivery_type_id": product_id[-1],
                            "volume": cols[4],
                            "total": cols[5],
                            "count": cols[-1],
                            "date": item["date"],
                            "created_on": None,
                            "updated_on": None,
                        })
                print(f"Обработана ссылка: {item}")

            except Exception as e:
                print(f"Ошибка при обработке файла {item['url']}: {e}")

        self.save_to_csv()

    def save_to_csv(self, filename="spimex_trading_results.csv"):
        with open("spimex_trading_results.csv",  mode='w', encoding='utf-8-sig', newline='') as file:
            fieldnames = [
                'exchange_product_id',
                'exchange_product_name',
                'oil_id',
                "delivery_basis_id",
                "delivery_basis_name",
                "delivery_type_id",
                "volume",
                "total",
                "count",
                "date",
                "created_on",
                "updated_on"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            writer.writerows(self.all_data)

    def run(self):
        self.parse_links()
        self.save_links()
        self.parse_xls()


if __name__ == "__main__":
    start = datetime.now()
    parser = ParserTrade()
    parser.run()
    end = datetime.now()
    print(f"Затраченное время: {end-start}")
    #Затраченное время: 0:05:45.793918
