import requests
import codecs
from bs4 import BeautifulSoup as BS
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8'}
'''h = codecs.open('krskbezformata.html', 'w', 'utf-8')
h.write(str(resp.text))
h.close()'''
def sportuspro(url):
    news = []
    errors = []
    resp = requests.get(url, headers=headers)
    domain = 'https://sportus.pro/'
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', class_='row-no-gutter')
        if main_div:
            div_lst = main_div.find_all('div', class_='col-xs-12')
            for div in div_lst:
                div_without_picture = div.find('div', class_='post-body')
                div_container = div_without_picture.div.find('div', class_='post-title')
                title = div_container.find('h6')
                href = title.a['href']
                description = div_container.p.text
                news.append({'title': title.text, 'url': domain + href,
                             'description': description})
        else:
            errors.append({'url': url, 'title': 'Div doesn’t exists'})
    else:
        errors.append({'url': url, 'title': 'Page don’t response'})
    return news, errors
def bezformata(url):
    news = []
    errors = []
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_section = soup.find('section', class_='listtopicbox')
        if main_section:
            article_lst = main_section.find_all('article', class_='listtopicline')
            for article in article_lst:
                before_title = article.find('a', attrs={'itemprop': 'url'})
                title = before_title.find('h3')
                href = article.a['href']
                description = article.find('div', attrs={'itemprop': 'description'})
                news.append({'url': href, 'title': title.text,
                             'description': description.text})
        else:
            errors.append({'url': url, 'title': 'Div doesn’t exists'})
    else:
        errors.append({'url': url, 'title': 'Page don’t response'})
    return news, errors
if __name__ == '__main__':
    url = 'https://krasnoyarsk.bezformata.com/sport/'
    news, errors = bezformata(url)
    h = codecs.open('bezformata.txt', 'w', 'utf-8')
    h.write(str(news))
    h.close()