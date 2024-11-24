from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Employer
from .forms import StudentProfileForm, EmployerProfileForm
from django.contrib.auth import logout
from .models import Job
from .forms import JobForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from django.views.generic.detail import DetailView

@login_required
def profile_view(request):
    # Проверяем роль пользователя и получаем профиль
    if request.user.role == 'student':
        profile = get_object_or_404(Student, user=request.user)
        template = 'student.html'  # Шаблон для студента
    elif request.user.role == 'employer':
        profile = get_object_or_404(Employer, user=request.user)
        template = 'employer.html'  # Шаблон для работодателя
    else:
        # Если роль не определена, возвращаем ошибку или страницу по умолчанию
        return render(request, 'profile_default.html', {'message': 'Роль не определена.'})

    # Рендерим нужный шаблон с профилем
    return render(request, template, {'profile': profile})

@login_required
def edit_profile(request):
    if request.user.role == 'student':
        profile = Student.objects.get(user=request.user)
        form = StudentProfileForm(instance=profile)
    elif request.user.role == 'employer':
        profile = Employer.objects.get(user=request.user)
        form = EmployerProfileForm(instance=profile)
    else:
        return redirect('profile')

    if request.method == 'POST':
        if request.user.role == 'student':
            form = StudentProfileForm(request.POST, instance=profile)
        elif request.user.role == 'employer':
            form = EmployerProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'edit_profile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('reg') 


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect("profile")  # Перенаправить на страницу профиля
    else:
        form = JobForm()
    return render(request, "employer/create_job.html", {"form": form})


@login_required
def view_applicants(request, job_id):
    job = Job.objects.get(id=job_id, employer=request.user)
    applicants = job.applicants.all()
    return render(request, "employer/view_applicants.html", {"job": job, "applicants": applicants})

@login_required
def employer_profile(request):
    if request.user.role != 'employer':
        return redirect('profile')

    jobs = Job.objects.filter(employer=request.user).order_by('-posted_at')
    return render(request, 'employer_profile.html', {
        'user': request.user,
        'profile': request.user.profile,
        'jobs': jobs
    })



@login_required
def create_job(request):
    if request.user.role != 'employer':  # Проверяем, что это работодатель
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # Привязываем вакансию к работодателю
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'create_job.html', {'form': form})



class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'  # Укажите ваш шаблон
    context_object_name = 'job'       # Название переменной, используемой в шаблоне


def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})

# Детали вакансии + отклик
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST' and request.user.role == 'student':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'job_detail.html', {'job': job, 'form': form})


