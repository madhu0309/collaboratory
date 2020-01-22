from django.contrib import admin
from collab_app import models
# Register your models here.

admin.site.register(models.Question)
admin.site.register(models.Answer)