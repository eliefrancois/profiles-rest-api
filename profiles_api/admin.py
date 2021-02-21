from django.contrib import admin
from profiles_api import models # importing models from the profiles api app

admin.site.register(models.UserProfile)
