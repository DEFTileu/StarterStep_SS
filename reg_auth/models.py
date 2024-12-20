from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employer', 'Employer'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Обязательное поле для работы админки
    is_superuser = models.BooleanField(default=False)  # Обязательное поле для PermissionsMixin

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Поле для аутентификации
    REQUIRED_FIELDS = ['name']  # Обязательные поля для суперпользователя

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Имеет ли пользователь конкретное разрешение."""
        return True

    def has_module_perms(self, app_label):
        """Имеет ли пользователь доступ к указанному приложению."""
        return True
