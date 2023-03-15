from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def is_commercial(self):
        """Return True if the user is in the Commercial Group or False"""
        if not hasattr(self, '_is_commercial'):
            self._is_commercial = self.groups.filter(
                name="commercial").exists()
            return self._is_commercial


    def is_support(self):
        """Return True if the user is in the Support Group or False"""
        if not hasattr(self, '_is_support'):
            self._is_support = self.groups.filter(
                name="support").exists()
            return self._is_support
    
    def __str__(self):
        if self.groups.exists():
            return f"id: {self.pk}, email :{self.email}, group: {''.join(self.groups.all().values_list('name', flat=True))}"
        elif self.is_superuser:
            return f"id: {self.pk}, email :{self.email}, group: manager"
        else:
            return f"id: {self.pk}, email :{self.email}, /!\ User is not assigned to a group /!\ "