from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from Profilee.models import Student, Employer
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Profilee.forms import StudentProfileForm, EmployerProfileForm


def auth_page(request):
    register_form = UserForm()

    if request.method == 'POST':
        # Регистрация
        if 'register' in request.POST:
            register_form = UserForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.password = make_password(register_form.cleaned_data['password'])  # Хэшируем пароль
                user.save()

                # Создаем профиль студента или работодателя
                if user.role == 'student':
                    Student.objects.create(user=user)
                elif user.role == 'employer':
                    Employer.objects.create(user=user)

                messages.success(request, "Registration successful! You can now log in.")
                return redirect('reg')

        # Авторизация
        elif 'login' in request.POST:
            email = request.POST.get('email-login')
            password = request.POST.get('password-login')
            user = authenticate(request, username=email, password=password)  # Используем email для логина
            if user is not None:
                login(request, user)
                return redirect('profile')  # Перенаправляем на профиль
            else:
                messages.error(request, "Invalid email or password")

    return render(request, 'register.html', {
        'register_form': register_form,
    })



