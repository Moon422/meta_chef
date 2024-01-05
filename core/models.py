from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
# class Address(models.Model):
#     house_number = models.CharField(null=False)
#     road_number = models.CharField(null=False)
#     block_number = models.CharField(null=False)
#     post_office = models.CharField(null=False)
#     police_station = models.CharField(null=False)
#     district = models.CharField(null=False)

#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

class ProfileType(models.IntegerChoices):
    ADMIN = (0, 'admin')
    KITCHEN_OWNER = (1, 'kitchen_owner')
    DELIVERY_PERSON = (2, 'delivery_person')
    CUSTOMER = (3, 'customer')

class Profile(models.Model):
    phonenumber = models.CharField(max_length=14, null=False)
    house_number = models.CharField(null=False)
    road_number = models.CharField(null=False)
    block_number = models.CharField(null=False)
    post_office = models.CharField(null=False)
    police_station = models.CharField(null=False)
    district = models.CharField(null=False)
    profile_type = models.IntegerField(
        choices=ProfileType.choices, default=ProfileType.CUSTOMER)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Kitchen(models.Model):
    name = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
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
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
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
    viewer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    view_date = models.DateTimeField(null=False)
    view_count = models.IntegerField(null=False, default=1)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
