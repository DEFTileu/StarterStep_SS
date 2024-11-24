from django.db import models
from reg_auth.models import User

class Student(models.Model):
    user = models.OneToOneField(
        'reg_auth.User', 
        on_delete=models.CASCADE, 
        related_name='student'
    )
    university = models.CharField(max_length=255, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)



class Employer(models.Model):
    user = models.OneToOneField(
        'reg_auth.User', 
        on_delete=models.CASCADE, 
        related_name='employer'
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    open_positions = models.TextField(blank=True, null=True)


from django.db import models
from reg_auth.models import User

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')  # Связь с работодателем
    title = models.CharField(max_length=200)  # Название вакансии
    description = models.TextField()  # Описание вакансии
    location = models.CharField(max_length=100)  # Местоположение
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Зарплата
    posted_at = models.DateTimeField(auto_now_add=True)  # Дата создания вакансии

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')  # Связь с вакансией
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')  # Студент
    cover_letter = models.TextField()  # Сопроводительное письмо
    applied_at = models.DateTimeField(auto_now_add=True)  # Дата отклика

    def __str__(self):
        return f'{self.student.username} -> {self.job.title}'

