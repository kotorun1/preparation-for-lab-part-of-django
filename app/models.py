from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150)
    fio = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "fio"]


# Products

class Product(models.Model):
    name = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=366)
    price = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_price = models.IntegerField(default=0)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
