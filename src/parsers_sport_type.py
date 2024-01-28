import requests
import codecs
from bs4 import BeautifulSoup as BS
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'}
'''h = codecs.open('sport24.html', 'w', 'utf-8')
h.write(str(resp.text))
h.close()'''
def sovsport(url):
    news = []
    errors = []
    domain = 'https://www.sovsport.ru'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', class_='content-widget-line_root__57xs_')
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'content-widget-line-item_grid-item__O1JP3'})
            for div in div_lst:
                href = div.a['href']
                divs_without_picture = div.a.span.span.div.div.find('div', attrs={'class': 'content-widget-line-item_main-content__SMzOP'})
                before_sport_type = divs_without_picture.find('div', class_='content-widget-line-item_header__9f_JO')
                sport_type = before_sport_type.find('span', class_='typography-module__font-text-block--Z4rA2')
                title = divs_without_picture.find('div', attrs={'class': 'content-widget-line-item_truncate___zJNC'}).find('span')
                before_description = divs_without_picture.find_all('div')[2]
                description = before_description.find('span')
                news.append({'sport_type': sport_type, 'title': title.text,
                             'url': domain+href, 'description': description})
        else:
            errors.append({'url': url, 'title': 'Div doesn’t exists'})
    else:
        errors.append({'url': url, 'title': 'Page don’t response'})
    return news, errors
def sport24(url):
    news = []
    errors = []
    domain = 'https://sport24.ru/'
    url = 'https://sport24.ru/mma'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        before_main_div = soup.find('div', class_='ey527T')
        main_div = before_main_div.find('div', class_='RSavmX')
        if main_div:
            div_lst = main_div.find_all('div', class_='p4EtJn')
            for div in div_lst:
                article = div.find('article')
                title = article.h3.a.find('span')
                href = article.h3.a['href']
                description = article.find('div', class_='DPnycC')
                before_sport_type = article.find('div', class_='ewCiiz')
                sport_type = before_sport_type.find('a')
                news.append({'title': title.text, 'url': domain + href,
                             'description': description, 'sport_type': sport_type.text})
        else:
            errors.append({'url': url, 'title': "Div doesn't exists"})
    else:
        errors.append({'url': url, 'title': "Page don't response"})
    return news, errors
if __name__ == '__main__':
    url = 'https://www.sovsport.ru/football'
    news, errors = sovsport(url)
    h = codecs.open('sovsport.txt', 'w', 'utf-8')
    h.write(str(news))
    h.close()