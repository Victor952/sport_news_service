from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from  django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm_city, UserUpdateForm_st, ContactForm_st, ContactForm_city
from sport_news.models import Error
import datetime as dt
User = get_user_model()
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')
def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему')
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})
def update_view(request):
    contact_form_st = ContactForm_st()
    contact_form_city = ContactForm_city()
    if request.user.is_authenticated:  # проверка регистрации и авторизации пользователя
        user = request.user
        if request.method == 'POST':  # "отправляем данные на проверку"
            form_st = UserUpdateForm_st(request.POST)
            form_city = UserUpdateForm_city(request.POST)
            if form_st.is_valid():
                data = form_st.cleaned_data
                user.stype = data['stype']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены')
                return redirect('accounts:update_st')
            if form_city.is_valid():
                data = form_city.cleaned_data
                user.city = data['city']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены')
                return redirect('accounts:update_city')
        form_st = UserUpdateForm_st(
            initial={'stype': user.stype, 'send_email': user.send_email})
        form_city = UserUpdateForm_city(
            initial={'city': user.city, 'send_email': user.send_email})
        return render(request, 'accounts/update.html',
                      {'form_city': form_city, 'contact_form_city': contact_form_city,
                       'form_st': form_st, 'contact_form_st': contact_form_st})
    else:
        return redirect('accounts:login')
def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён :(')
    return redirect('home')
def contact(request):
    if request.method == 'POST':
        contact_form_city = ContactForm_city(request.POST or None)
        contact_form_st = ContactForm_st(request.POST or None)
        if contact_form_city.is_valid():
            data = contact_form_city.cleaned_data
            city = data.get('city')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists:
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [{'city': city, 'email': email}]}
                Error(data=data).save()
            messages.success(request, 'Данные отправлены администрации')
            return redirect('accounts:update')
        elif contact_form_st.is_valid():
            data = contact_form_st.cleaned_data
            stype = data.get('stype')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists:
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'stype': stype, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [{'stype': stype, 'email': email}]}
                Error(data=data).save()
            messages.success(request, 'Данные отправлены администрации')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')