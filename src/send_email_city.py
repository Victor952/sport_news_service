import os, sys
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
import django
import datetime
from sport_news.models import Newsc, Error, Url
from sport_news_service.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD
ADMIN_USER = EMAIL_HOST_USER
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "sport_news_service.settings"
django.setup()
today = datetime.date.today()
subject = f"Рассылка спортивных новостей {today}"
text_content = f"Рассылка новостей {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению, на сегодня по вашим предпочтениям данных нет</h2>'
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'email')  # метод values вызывается один раз
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city']))
    users_dct[(i['city'])].append(i['email'])
if users_dct:
    params = {'city_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
    qs = Newsc.objects.filter(**params, timestamp=today).values()[:10]
    news = {}
    for i in qs:
        news.setdefault((i['city_id']), [])
        news[(i['city_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = news.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h3>'
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
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p><a href="{ i["url"] }">Error: { i["title"] }</a></p>'
    subject = f"Ошибки скрапинга {today}"
    text_content = f"Ошибки скрапинга"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
        for i in data:
            _html += f'<p>Город: {i["city"]}, Электронная почта: {i["email"]}</p>'
        subject = f"Пожелания пользователей {today}"
        text_content = f"Пожелания пользователей"
qs = Url.objects.all().values('city')
urls_dct = {(i['city']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0]:
            urls_err += f'<p>Для города:{ keys[0] } отсутствуют ссылки</p><br>'
if urls_err:
    subject += 'Отсутствуюшие ссылки'
    _html += urls_err
if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()