from django.contrib import admin
from .models import Fabricante, Proveedor, Estado, Ubicacion, Base, Reactivo, Orden, Detalle_Orden, Unidad, Lugar, Fase, Codigo, Cantidad, Consecutivo, Consumo

# Register your models here.
# Se puede realizar CRUD de las tablas a continuacion en Admin
admin.site.register(Fase)
admin.site.register(Fabricante)
admin.site.register(Proveedor)
admin.site.register(Estado)
admin.site.register(Lugar)
admin.site.register(Ubicacion)
admin.site.register(Base)
admin.site.register(Codigo)
admin.site.register(Reactivo)
admin.site.register(Orden)
admin.site.register(Detalle_Orden)
admin.site.register(Unidad)
admin.site.register(Cantidad)
admin.site.register(Consecutivo)
admin.site.register(Consumo)