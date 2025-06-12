from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


# Строка подключения к твоей БД
DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydb"

# Создаём движок
engine = create_engine(DATABASE_URL)

# Проверяем подключение
try:
    conn = engine.connect()
    print("Успешное подключение к базе данных!")
    conn.close()
except Exception as e:
    print("Ошибка подключения:", str(e))
    
    
Base.metadata.create_all(engine)

print("Все таблицы упешно созданы в БД")