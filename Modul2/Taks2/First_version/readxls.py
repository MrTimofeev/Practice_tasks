import requests
import json
import xlrd
import pprint
import csv

ALL_DATA = []

with open('news.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


for i in data:
    responce = requests.get(i["url"])

    with open('file.xls', "wb") as file:
        file.write(responce.content)

    book = xlrd.open_workbook("file.xls")

    shet = book.sheet_by_index(0)

    for row in range(shet.nrows):
        if len(shet.row_values(row)[1]) == 11 and shet.row_values(row)[-1].isdigit():
            exchange_product_id = shet.row_values(row)[1]
            exchange_product_name = shet.row_values(row)[2]
            delivery_basis_name = shet.row_values(row)[3]
            volume = shet.row_values(row)[4]
            total = shet.row_values(row)[5]
            count = shet.row_values(row)[-1]

            ALL_DATA.append({
                "exchange_product_id": exchange_product_id,
                "exchange_product_name": exchange_product_name,
                "oil_id":  exchange_product_id[:4],
                "delivery_basis_id": exchange_product_id[4:7],
                "delivery_basis_name": delivery_basis_name,
                "delivery_type_id": exchange_product_id[-1],
                "volume": volume,
                "total": total,
                "count": count,
                "date": i["date"],
                "created_on": None,
                "updated_on": None,
            })
    print(f"Обработана ссылка: {i}")

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
    
    writer.writeheader()        # Записываем заголовки
    writer.writerows(ALL_DATA)      # Записываем данные    