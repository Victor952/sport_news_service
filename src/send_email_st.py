import os, sys
from django.contrib.auth import get_user_model
import django
import datetime

from django.core.mail import EmailMultiAlternatives

from sport_news.models import Newsst, Error, Url
from sport_news_service.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD
ADMIN_USER = EMAIL_HOST_USER
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "sport_news_service.settings"
django.setup()
today = datetime.date.today()
subject = f"Рассылка спортивных новостей за {today}"
text_content = f"Рассылка новостей {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению, на сегодня по вашим предпочтениям данных нет</h2>'
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['stype']), [])
    users_dct[(i['stype'])].append(i['email'])
if users_dct:
    params = {'stype_id__in': []}
    for pair in users_dct.keys():
        params['stype_id__in'].append(pair[0])
    qs = Newsst.objects.filter(**params, timestamp=today).values()[:10]
    news = {}
    for i in qs:
        news.setdefault((i['stype_id']), [])
        news[(i['stype_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = news.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            # отправка писем для пользователей-подписчиков
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():  # если какие-то ошибки есть на этот день
    error = qs.first
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{ i["url"] }">Error: { ["title"] }</a></p>'
    subject = f"Ошибки скрапинга {today}"
    text_content = f"Ошибки скрапинга"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>Вид спорта: {i["stype"]}, Электронная почта: {i["email"]}</p>'
        subject = f"Пожелания пользователей {today}"
        text_content = f"Пожелания пользователей"
qs = Url.objects.all().values('stype')
urls_dct = {(i['stype']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0]:
            urls_err += f'<p>Для вида спорта:{ keys[0] } отсутствуют ссылки</p><br>'
if urls_err:
    subject += 'Отсутствуюшие ссылки'
    _html += urls_err
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()