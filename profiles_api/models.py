from django.db import models
from django.conf import settings # used to retreive AUTH_USER_MODEL from settings.py file

# These two imports allow for the default user model to be customized or overrided 
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import PermissionsMixin

# Default model manager
from django.contrib.auth.models import BaseUserManager 


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
            

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for patients in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


class PatientInfo(models.Model):
    """Database model for patient information"""

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, # This points to the usermodel used for authentication in settings.py, if we need to change the model used change it there
        on_delete=models.CASCADE
    )

    # Patient insulin injected choices
    YES = 'YES'
    NO = 'NO'

    IS_INSULIN_INJECTED_CHOICES = [
        (YES, 'YES'),
        (NO, 'NO'),
    ]

    inject_date = models.DateField(auto_now_add=True, auto_now=False, blank= False)
    inject_time = models.TimeField(auto_now_add=True, auto_now=False, blank= False)
    blood_sugar_level = models.CharField(max_length=20, blank= False)
    is_insulin_injected = models.CharField(choices = IS_INSULIN_INJECTED_CHOICES, default = 1, max_length=3, blank= False)
    quantity = models.CharField(max_length=10, blank= False)
    inject_area = models.TextField(blank= False)

