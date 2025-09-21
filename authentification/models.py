from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        if not role:
            raise ValueError("Le rôle est obligatoire (entreprise ou freelance)")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, role=User.ROLE_ADMIN, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_ADMIN = 'Admin'
    ROLE_ENTREPRISE = 'Entreprise'
    ROLE_FREELANCE = 'Freelance'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_ENTREPRISE, 'Entreprise'),
        (ROLE_FREELANCE, 'Freelance'),
    ]

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField('Email', unique=True)
    role = models.CharField('Rôle', max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # rôle obligatoire lors de la création

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
