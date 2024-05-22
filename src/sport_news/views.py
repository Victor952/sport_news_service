from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import FindForm_city, FindForm_st
from .models import Newsc, Newsst
def home_view(request):
    form_city = FindForm_city()
    form_st = FindForm_st()
    return render(request, 'sport_news/home.html',
                  {'form_city': form_city, 'form_st': form_st})
def list_view_st(request):
    form_st = FindForm_st()
    stype = request.GET.get('stype')
    _filter_st = {}
    if stype:
        context_st = {'stype': stype, 'form_st': form_st}
        _filter_st['stype__slug'] = stype
        qs_st = Newsst.objects.filter(**_filter_st)
        paginator_st = Paginator(qs_st, 10)
        page_number_st = request.GET.get('page')
        page_obj_st = paginator_st.get_page(page_number_st)
        context_st['object_list_st'] = page_obj_st
        return render(request, 'sport_news/list_st.html', context_st)
def list_view_c(request):
    form_city = FindForm_city()
    city = request.GET.get('city')
    _filter_city = {}
    if city:
        context_c = {'city': city, 'form_city': form_city}
        _filter_city['city__slug'] = city
        qs_c = Newsc.objects.filter(**_filter_city)
        paginator_c = Paginator(qs_c, 10)
        page_number_c = request.GET.get('page')
        page_obj_c = paginator_c.get_page(page_number_c)
        context_c['object_list_c'] = page_obj_c
        return render(request, 'sport_news/list_c.html', context_c)