from django.db import models

# Create your models here.
class Pedido (models.Model):
    date = models.DateTimeField(auto_now_add=True)
    cellphone = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    restaurant = models.CharField(max_length=20, default="")
    sucursal = models.CharField(max_length=50)
    delivery = models.CharField(max_length=500)
    direction = models.CharField(max_length=100)
    state = models.BooleanField(default=False)

class Sucursal (models.Model):
    user = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20)
    sucursal = models.CharField(max_length=20)
    password = models.CharField(max_length=20)