from django.shortcuts import render
from .models import News
def home_view(request):
    city = request.GET.get('city')
    sport_type = request.GET.get('sport_type')
    qs = []
    if city or sport_type:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if sport_type:
            _filter['sport_type__name'] = sport_type
    qs = News.objects.filter(**_filter)
    return render(request, 'sport_news/home.html', {'object_list': qs})
