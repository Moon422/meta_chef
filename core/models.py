from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Kitchen(models.Model):
    name = models.CharField(max_length=255, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=100, null=False)
    foods = models.ManyToManyField("Food", through="FoodCategory")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class Food(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1024, null=False)
    price = models.FloatField(null=False)
    image_url = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, through="FoodCategory")
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class FoodCategory(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Ratings(models.IntegerChoices):
    ZERO = 0, 'zero'
    ONE = 1, 'one'
    TWO = 2, 'two'
    THREE = 3, 'three'
    FOUR = 4, 'four'
    FIVE = 5, 'five'

class Rating(models.Model):
    rating = models.IntegerField(null=False, default=Ratings.FIVE, choices=Ratings.choices)
    food = models.ForeignKey(Food, null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class OrderStatus(models.IntegerChoices):
    NOT_PLACED = 0
    ORDER_PLACED = 1
    DELIVERED = 2


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=14, null=False)
    discount = models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0)
    orderstatus = models.IntegerField(
        choices=OrderStatus.choices, default=OrderStatus.NOT_PLACED)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.FloatField(default=0)
    review_submitted = models.BooleanField(default=False)
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class FoodViewed(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
