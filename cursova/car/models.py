import uuid

from django.db import models
from django.utils import timezone

from auth_user.models import CustomUser


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    cars = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    body_type = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    engine_capacity = models.FloatField()
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    price = models.FloatField()
    mileage = models.FloatField()
    available = models.BooleanField()
    img = models.CharField(max_length=255)
    discount = models.FloatField()
    def final_price(self):
        if self.discount != 0 and self.discount < self.price:
            return self.price - self.discount
        return self.price


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    price = models.FloatField()
    status = models.CharField(max_length=255, default='Pending')

    def color(self):
        if self.status == 'Pending':
            return 'warning'
        elif self.status == 'Confirmed':
            return 'primary'
        elif self.status == 'Preparing for delivery':
            return 'info'
        elif self.status == 'Delivered':
            return 'success'
        elif self.status == 'Canceled':
            return 'danger'

