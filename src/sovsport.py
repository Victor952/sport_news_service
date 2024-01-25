import requests
import codecs
from bs4 import BeautifulSoup as BS
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'}
domain = 'https://www.sovsport.ru'
url = 'https://www.sovsport.ru/football'
resp = requests.get(url, headers=headers)
news = []
errors =[]
if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', class_='content-widget-line_root__57xs_')
    if main_div:
        div_lst = main_div.find_all('div', attrs={'class': 'content-widget-line-item_grid-item__O1JP3'})
        for div in div_lst:
            href = div.a['href']
            divs_without_picture = div.a.span.span.div.div.find('div', attrs={'class': 'content-widget-line-item_main-content__SMzOP'})
            title = divs_without_picture.find('div', attrs={'class': 'content-widget-line-item_truncate___zJNC'}).find('span')
            description = divs_without_picture.find_all('span')[2]
            news.append({'title': title.text, 'url': domain+href,
                         'description': description})
    else:
        errors.append({'url': url, 'title': 'Div doesn’t exists'})
else:
    errors.append({'url': url, 'title': 'Page don’t response'})
h = codecs.open('sovsport.txt', 'w', 'utf-8')
h.write(str(news))
h.close()