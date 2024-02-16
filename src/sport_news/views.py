from django.shortcuts import render
from .forms import FindForm_city, FindForm_st
from .models import News
def home_view(request):
    form_city = FindForm_city()
    form_st = FindForm_st()
    city = request.GET.get('city')
    sport_type = request.GET.get('sport_type')
    qs = []
    if city or sport_type:
        _filter_city = {}
        _filter_st = {}
        if city:
            _filter_city['city__slug'] = city
        if sport_type:
            _filter_st['sport_type__slug'] = sport_type
        qs = News.objects.filter(**_filter_city, **_filter_st)
    return render(request, 'sport_news/home.html',
                  {'object_list': qs, 'form_city': form_city, 'form_st': form_st})