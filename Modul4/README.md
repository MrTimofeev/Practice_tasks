### Решение практики модуля 4

### Начало работы

#### 1. Установите зависимости
``` bash
pip install -r requirements.txt
```

#### 2. Создайте файл `.env`

``` env
DATABASE_URL=postgresql+asyncpg://parser_user:parser_pass@localhost:5432/parser_db
```

#### 3. Запустите PostgreSQL через Docker

``` bash
docker-compose up -d
```

#### 4. Запустите парсер
``` bash
python Modul4/async_parse.py
```