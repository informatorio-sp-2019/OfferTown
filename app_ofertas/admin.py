from django.contrib import admin
from app_ofertas import models
# Register your models here.

class LocalidadAdmin(admin.ModelAdmin):
	pass

class LocalAdmin(admin.ModelAdmin):
	pass

class SucursalAdmin(admin.ModelAdmin):
	pass

class HorarioAdmin(admin.ModelAdmin):
	pass

class RubroAdmin(admin.ModelAdmin):
	pass

class PublicacionAdmin(admin.ModelAdmin):
	pass

class FavoritoAdmin(admin.ModelAdmin):
	pass

class InteresAdmin(admin.ModelAdmin):
	pass



admin.site.register(models.Localidad,LocalidadAdmin)
admin.site.register(models.Local,LocalAdmin)
admin.site.register(models.Sucursal,SucursalAdmin)
admin.site.register(models.Horario,HorarioAdmin)
admin.site.register(models.Rubro,RubroAdmin)
admin.site.register(models.Publicacion,PublicacionAdmin)
admin.site.register(models.Favorito,FavoritoAdmin)
admin.site.register(models.Interes,InteresAdmin)
admin.site.register(models.Usuario)
admin.site.register(models.MedioDePago)
admin.site.register(models.LocalMedioDePago)
