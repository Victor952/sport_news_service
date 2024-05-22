import asyncio
import codecs
import os
import sys
from django.contrib.auth import get_user_model
from django.db import DatabaseError
import datetime as dt
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "sport_news_service.settings"
import django
django.setup()
from sport_news.parsers_city import *
from sport_news.models import Newsc, Url, Error

User = get_user_model()
parsers = (
    (sportuspro, 'sportus'),
    (bezformata, 'bezformata')
)
news, errors = [], []
def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id']) for q in qs)
    return settings_lst
def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}; tmp['city'] = pair[0]
            tmp['url_data'] = url_dct[pair]; urls.append(tmp)
    return urls
async def main(value):
    func, url, city = value
    new, err = await loop.run_in_executor(None, func, url, city)
    errors.extend(err)
    news.extend(new)
settings = get_settings(); url_list = get_urls(settings)
loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
'''for func, url in parsers:
    n, e = func(url)
    news += n
    errors += e'''
loop.run_until_complete(tasks)
loop.close()
for new in news:
    v = Newsc(**new)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())  # если в этот день появились новые новости
    if qs.exists:
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()
# h = codecs.open('tomskrosrab.txt', 'w', 'utf-8')
# h.write(str(jobs)); h.close()
ten_days_ago = dt.date.today() - dt.timedelta(10)
Newsc.objects.filter(timestamp__lte=ten_days_ago).delete()