from django.contrib import admin

# Register your models here.
from .models import Pedido, Sucursal

admin.site.register(Pedido)
admin.site.register(Sucursal)