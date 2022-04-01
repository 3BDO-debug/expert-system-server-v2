from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.DiagnoseReport)
admin.site.register(models.DiagnoseResult)
