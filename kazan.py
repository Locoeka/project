import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

urls = ['https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=264&engine_version=2&offer_type=flat&p={}&room1=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=264&engine_version=2&offer_type=flat&p={}&room2=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=264&engine_version=2&offer_type=flat&p={}&room3=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}&region=4777&room4=1&room5=1&room6=1&room7=1&room9=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=258&district%5B1%5D=259&engine_version=2&offer_type=flat&p={}&room1=1&room2=1&room3=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=261&engine_version=2&offer_type=flat&p={}&room1=1&room2=1&room3=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=262&engine_version=2&offer_type=flat&p={}&room1=1&room2=1&room3=1&with_neighbors=0',
       'https://kazan.cian.ru/cat.php?deal_type=sale&district%5B0%5D=263&engine_version=2&offer_type=flat&p={}&room1=1&room2=1&room3=1&with_neighbors=0']

def page_grabber(page):
    flats_links = [] 
    p = len(page)
    for i in range(p):
        flats_links.append(page[i].attrs['href']) 
    return(flats_links)

links = [] # Список, который заполним всеми квартирами

for url in urls:
    for i in range(0,55):
        
        search_page = requests.get(url.format(i))
        search_page = search_page.text
        search_page = BeautifulSoup(search_page, 'lxml')
        
        flats = search_page.html.body.findAll('a', attrs = {'class':'_93444fe79c--link--39cNw'})
        
        links = links + page_grabber(flats)
        print('Page {} is working well'.format(i))		


ulinks = set(links) # смотрим только уникальные ссылки на предложения	

flats_dict = {}
N = 0


for l in ulinks:
    
    # Номер квартиры
    N = N + 1

    flat_page = requests.get(l)
    flat_page = flat_page.text
    flat_page = BeautifulSoup(flat_page, 'lxml')
   
    inf_main = flat_page.findAll('div', {'class':'a10a3f92e9--info-value--18c8R'})
    inf_main_n = flat_page.findAll('div', {'class':'a10a3f92e9--info-title--2bXM9'})
    
    sp_d = {}
    for i in range(0,len(inf_main)):
        sp_d[inf_main_n[i].text] = re.findall(r'\d+', inf_main[i].text)[0]

    inf_gen = flat_page.findAll('span', {'class':'a10a3f92e9--value--3Ftu5'})
    inf_gen_n = flat_page.findAll('span', {'class':'a10a3f92e9--name--3bt8k'})

    for i in range(0,len(inf_gen)):
        sp_d[inf_gen_n[i].text] = inf_gen[i].text

    inf_price = flat_page.find('span', {'itemprop':'price'})
    sp_d['Цена'] =''.join(re.findall(r'\d+', inf_price.text))

    inf_room = flat_page.find('h1', {'class':'a10a3f92e9--title--2Widg'})
    sp_d['Комнат'] = inf_room.text[0:7]

    inf_area = flat_page.findAll('a', {'class':'a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr'})
    sp_d['Район'] = re.findall(r"р-н +\w+", str(inf_area))[0]
    
    sp_d['Линк'] = l
    
    flats_dict[N] = sp_d
    print('Page {} is working well'.format(N))

	

df_flats = pd.DataFrame(flats_dict).T
df_flats.to_csv('CIAN.csv', encoding="utf-8-sig")
df_flats
