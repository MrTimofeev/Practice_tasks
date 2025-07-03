from bs4 import BeautifulSoup
from datetime import datetime
import json
import xlrd
import io
import asyncio
import aiohttp
import aiofiles
from models import ParserData
from database import engine, Base, AsyncSessionLocal
from sqlalchemy import insert


class ParserTrade():

    def __init__(self, max_pages=100, min_date=datetime(2023, 1, 1), concurrency=3):
        self.max_pages = max_pages
        self.min_date = min_date
        self.base_url = "https://spimex.com"
        self.all_links = []
        self.all_data = []
        self.count = 1
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)

    async def generate_urls(self):
        """Генерирует список URL для обработки"""
        for page in range(1, self.max_pages + 1):
            yield f"{self.base_url}/markets/oil_products/trades/results/?page=page-{page}&bxajaxid=d609bce6ada86eff0b6f7e49e6bae904"

    async def create_tasks(self, session):
        """ Создает задачи для всех URL"""
        tasks = []
        async for url in self.generate_urls():
            tasks.append(asyncio.create_task(self._fetch_page(session, url)))
        return tasks

    async def _fetch_page(self, session, url):
        """Делает запрос и парсит страницу"""
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        self._append_all_links(content)
                    else:
                        print(
                            f"ошибка при загрузке страницы {url}, статус: {response.status}")
            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")

    async def request_syte(self):
        """Запускает создание и выполнение задач"""
        connector = aiohttp.TCPConnector(limit_per_host=10, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = await self.create_tasks(session)
            await asyncio.gather(*tasks)

    def _append_all_links(self, response):
        """Достает все ссылки и сохраняет в all_links"""
        soup = BeautifulSoup(response, "lxml")
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
                break

            if "oil_xls" in url:
                self.all_links.append(
                    {"url": url, "date": date_span.text.strip()})

    async def save_links(self):
        """Сохраняет все ссылки в JSON"""
        data_srt = json.dumps(self.all_links, ensure_ascii=False, indent=4)
        async with aiofiles.open('news.json', 'w', encoding='utf-8') as file:
            await file.write(data_srt)

    async def load_links(self):
        """Достает все ссылки из JSON"""
        async with aiofiles.open('news.json', 'r', encoding='utf-8') as file:
            data_str = await file.read()
            data = json.loads(data_str)
            return data

    async def donwload_xls(self, session, url):
        """Скачивает файл по ссылке"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    return io.BytesIO(content)
                else:
                    print(
                        f"Ошибка при загрузке файла {url}, статус: {response.status}")
                    raise Exception(f'Ошибка загрузки {url}')
        except Exception as e:
            print(f"Ошибка при загрузке: {url}: {e}")

    async def _init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы и проверены")

    async def save_to_db(self, session, data_list: dict):
        stmt = insert(ParserData).values(data_list)
        try:
            await session.execute(stmt)
            await session.commit()
            print(f"Сохраннено {len(data_list)} записей")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при сохранении: {e}")

    async def process_file(self, session_http, item):
        """Обрабатывает скачаный файл"""
        xls_data = await self.donwload_xls(session_http, item["url"])
        if not xls_data:
            return

        try:
            book = xlrd.open_workbook(file_contents=xls_data.getvalue())
            shet = book.sheet_by_index(0)
            
            data_list = []

            for row_num in range(shet.nrows):
                cols = shet.row_values(row_num)

                if len(cols) < 6:
                    continue

                product_id = cols[1]
                count = cols[-1]

                if len(product_id) == 11 and count.isdigit():
                    data_list.append(
                        {
                            "exchange_product_id": product_id,
                            "exchange_product_name": cols[2],
                            "oil_id":  product_id[:4],
                            "delivery_basis_id": product_id[4:7],
                            "delivery_basis_name": cols[3],
                            "delivery_type_id": product_id[-1],
                            "volume": int(cols[4]),
                            "total": int(cols[5]) if not "." in cols[5] else int(cols[5].split(".")[0]),
                            "count": int(cols[-1]) ,
                            "date": datetime.strptime(item["date"], "%d.%m.%Y").date(),
                            "created_on": None,
                            "updated_on": None
                        },
                    )
            if data_list:
                async with AsyncSessionLocal() as session_db:    
                    await self.save_to_db(session_db, data_list)
                
            print(f"Оaбработана ссылка: {item}")
        except Exception as e:
            print(f"Ошибка при обработке файла {item['url']}: {e}")

    async def parse_xls(self):
        """Запускает задачи по обработке файлов и их сохранения"""
        data = await self.load_links()

        connector = aiohttp.TCPConnector(limit_per_host=5, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.process_file(session, item) for item in data]
            await asyncio.gather(*tasks)

    async def run(self):
        await self.request_syte()
        await self.save_links()
        await self._init_db()
        await self.parse_xls()


if __name__ == "__main__":
    start = datetime.now()
    parser = ParserTrade()
    asyncio.run(parser.run())
    end = datetime.now()
    print(f"Затраченное время: {end-start}")
