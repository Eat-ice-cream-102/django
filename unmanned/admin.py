from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Purchase)
admin.site.register(models.InOrOut)
admin.site.register(models.Member)
admin.site.register(models.ConfirmString)
