from django.db import models

# These two imports allow for the default user model to be customized or overrided 
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import PermissionsMixin

# Default model manager
from django.contrib.auth.models import BaseUserManager 


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email,name, password=None):
        """Create a new user profile fucntion"""
        if not email:
            raise ValueError('User must have email address') # If the user tries to create a user without a email passed in it will display this message to user

        email = self.normalize_email(email) # This makes the second half of the email case insensitive
        user = self.model(email=email, name= name) # This creates a new model that the manager is representing, it will then makea new instance an dset the email and name to the values passed in by the user

        user.set_password(password) # This converts the password created by user to hash so the data is secure
        user.save(using=self._db)

        return user # returns newly created user

    def create_super_user(self,email,name, password): 
        """Create a super user with given details"""
        user = self.create_user(email,name,password)

        user.is_superuser = True # function defined in PermissionsMixin
        user.is_staff = True

        user.save(using=self._db)

        return user  
            

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system""" # Doc string to explain what this function is doing
    email = models.EmailField(max_length=255, unique=True) # allows for user to enetr email to a length of 255 and required to be a unique instance in the DB
    name = models.CharField(max_length=255) # each email will have a name with a max length of 255, does not have to be unique
    is_active = models.BooleanField(default=True) #determines if a user profile is activate or not, default set to True
    is_staff = models.BooleanField(default=False) # determines if user profile will have admin rights


    objects = UserProfileManager() # This allows us to use custom model with the Django CLI

    USERNAME_FIELD = 'email' # replaces username field with the user email
    REQUIRED_FILEDS = ['name'] # Makes the name variable a required field, email variable is defaultly  required field

    def get_full_name(self):
        """Retrive full name of user"""
        return self.name

    def get_short_name(self):
        """Retrive short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email