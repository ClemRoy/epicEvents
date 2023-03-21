from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)

# Create your models here.


class UserManager(BaseUserManager):
    """
        Creates and saves a User with the given email,and password.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        private function
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
        """
        Create and save a new User instance with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. If no password is provided,
                a random password will be generated and assigned to the user.
            **extra_fields: Additional fields to be saved on the User instance, such as
                first_name and last_name.

        Returns:
            User: The newly created User instance.

        Raises:
            ValueError: If no email is provided.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creates and saves a superuser with the given email and password.

    Args:
        email (str): The email address for the superuser.
        password (str): The password for the superuser.
        **extra_fields (dict): Additional fields to save with the superuser.

    Returns:
        User: The newly created superuser.

    Raises:
        ValueError: If the email is not provided.
    """
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
        """Override the default save method to save the User object in the database and return the object itself.

        Args:
            *args: Optional positional arguments to be passed to the parent class's save method.
            **kwargs: Optional keyword arguments to be passed to the parent class's save method.

        Returns:
            The saved User object.
        """
        super(User, self).save(*args, **kwargs)
        return self

    def is_commercial(self):
        """Return True if the user is in the Commercial Group or False"""
        if not hasattr(self, '_is_commercial'):
            self._is_commercial = self.groups.filter(name="commercial").exists()
        return self._is_commercial

    def is_support(self):
        """Return True if the user is in the Support Group or False"""
        if not hasattr(self, '_is_support'):
            self._is_support = self.groups.filter(
                name="support").exists()
        return self._is_support

    def full_name(self):
        """
        Returns the user's full name by concatenating their first name and last name.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Return a string representation of the User object.
        If the user belongs to one or more groups, the string representation will include the user's id, email, and group(s) name(s) as a comma-separated list.
        If the user is a superuser, the string representation will include the user's id, email, and a note that the user is a manager.
        If the user does not belong to any group, the string representation will include the user's id, email, and a warning that the user is not assigned to any group.
        """
        if self.groups.exists():
            return f"id: {self.pk}, email :{self.email}, group: {''.join(self.groups.all().values_list('name', flat=True))}"
        elif self.is_superuser:
            return f"id: {self.pk}, email :{self.email}, group: manager"
        else:
            return f"id: {self.pk}, email :{self.email}, /!\ User is not assigned to a group /!\ "
