from django.db import models

# Create your models here.
class Username (models.Model):
    name = models.CharField(max_length=15)
    cellphone = models.CharField(max_length=15)

    def __str__(self):
        return self.cellphone