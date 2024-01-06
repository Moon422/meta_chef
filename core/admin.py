from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Kitchen)
admin.site.register(models.Food)
admin.site.register(models.Category)
admin.site.register(models.FoodCategory)
admin.site.register(models.Rating)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.FoodViewed)
