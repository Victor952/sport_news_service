from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from sport_news.models import Stype, City
User = get_user_model()
class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()  # strip удаляет пробелы
        password = self.cleaned_data.get('password').strip()
        if email and password:  # наличие этих переменных
            qs = User.objects.filter(email=email)  # запрос к бд
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):  # преобразование передаваемого в виде обычного текста пароля в зашифровку
                raise forms.ValidationError('Пароль неверный!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключён!')
        return super(UserLoginForm, self).clean(*args, **kwargs)
class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Введите электронную почту',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('email', )
    def clean_password2(self):  # проверка равенства паролей
        data = self.cleaned_data
        if data['password'] != data['password']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']
class UserUpdateForm_city(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug',
        required=True, label='Город', empty_label='Город не выбран',
        widget=forms.Select(attrs={'class': 'form-control'}))
    send_email = forms.BooleanField(widget=forms.CheckboxInput,
                                    required=False, label='Получать рассылку')
    class Meta:
        model = User
        fields = ('city', 'send_email')
class UserUpdateForm_st(forms.Form):
    stype = forms.ModelChoiceField(
        queryset=Stype.objects.all(), to_field_name='slug',
        required=True, label='Вид спорта', empty_label='Вид спорта не выбран',
        widget=forms.Select(attrs={'class': 'form-control'}))
    send_email = forms.BooleanField(widget=forms.CheckboxInput,
                                    required=False, label='Получать рассылку')
    class Meta:
        model = User
        fields = ('stype', 'send_email')
class ContactForm_city(forms.Form):
    city = forms.CharField(required=True, label='Город',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        required=True, label='Введите электронную почту',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
class ContactForm_st(forms.Form):
    stype = forms.CharField(required=True, label='Вид спорта',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        required=True, label='Введите электронную почту',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

