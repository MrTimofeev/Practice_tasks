import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

ALL_LINK_XLS = []
COUNT = 1
flag = False


 
while True:
    
    responce = requests.get(f"https://spimex.com/markets/oil_products/trades/results/?page=page-{COUNT}&bxajaxid=d609bce6ada86eff0b6f7e49e6bae904")
    
    if responce.status_code == 200:
        soup = BeautifulSoup(responce.text, "lxml")
        
        links = soup.find_all('div', attrs={'class': 'accordeon-inner__item'})
        
        for link in links:
            
            url = "https://spimex.com" + link.find("a", attrs={'class': 'accordeon-inner__item-title link xls'})['href']
            date = link.find("span").text
            
            date_parsed = datetime.strptime(date, '%d.%m.%Y')
            
            # Устанавливаем нижнюю границу — 1 января 2023
            start_date = datetime(2023, 1, 1)
            
            if date_parsed >= start_date:
                print("Эта дата подходит!")
            else:
                print("Эта дата слишком старая.")
                flag = True
                break
   
            if "oil_xls" in url:
                ALL_LINK_XLS.append({"url": url, "date": date})
                
    COUNT += 1
    
    if flag:
        break
    
    
with open('news.json', 'w', encoding='utf-8') as file:
    # Записываем данные в формате JSON
    json.dump(ALL_LINK_XLS, file, ensure_ascii=False, indent=4)
    
    
print("Парсинг завершен, полученны ссылкина скачинвание xls")