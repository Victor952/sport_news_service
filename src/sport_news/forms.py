from django import forms
from .models import City, Stype
class FindForm_city(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug',
        required=False, label='Город', empty_label='Город не выбран',
        widget=forms.Select(attrs={'class': 'form-control'}))
class FindForm_st(forms.Form):
    stype = forms.ModelChoiceField(
        queryset=Stype.objects.all(), to_field_name='slug',
        required=False, label='Вид спорта', empty_label='Виды спорта',
        widget=forms.Select(attrs={'class': 'form-control'}))