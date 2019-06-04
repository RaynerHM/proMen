from django.contrib import admin
# Register your models here.
from Mensajeria.models import *
from django.contrib.auth.models import User


class Admin_Mensajeria_Interna(admin.ModelAdmin):
	list_display = [
		'id', 'codigo', 'recepcionista',  'sucursal', 'remitente_externo',
		'remitente','destinatario', 'descripcion', 'fecha_recibido',
		'fecha_entrega', 'comentario', 'observacion', 'prioridad', 'estado',
		'recibido_por', 'fecha_enviado', 'fecha_recibido_int',
		'hist_enviado_por', 'hist_recibido_por', 'hist_entregado_por'
	]
	ordering = ['-id']
	
	list_filter = ('estado', 'sucursal', 'fecha_entrega', 'hist_enviado_por',
		'hist_recibido_por', 'hist_entregado_por', 'remitente_externo'
	)

	search_fields = [
		'id', 'recepcionista__username', 'sucursal', 'remitente',
		'destinatario', 'descripcion', 'fecha_recibido',
		'observacion', 'estado', 'fecha_entrega', 'codigo'
	]

	class Meta:
		model = Mensajeria_Interna


admin.site.register(Mensajeria_Interna, Admin_Mensajeria_Interna)



class Admin_Mensajeria_Externa(admin.ModelAdmin):
	list_display = [
		'sucursal', 'recepcionista', 'codigo', 'mensajero',
		'fecha_envio_depto', 'hora_envio_depto', 'departamento',
		'encargado', 'entregado_por', 'descripcion', 'destinatario',
		'prioridad', 'hora_salida', 'hora_entrada', 'acuse', 'comentario',
		'archivo_acuses',
	]
	ordering = ['-id']
	
	list_filter = ('estado', 'sucursal','prioridad', 'fecha_envio_depto',
		'mensajero', 'departamento',
	)

	search_fields = [
		'id', 'recepcionista__username', 'sucursal',
		'destinatario', 'descripcion', 'mensajero',
		'fecha_envio_depto', 'entregado_por', 'hora_salida', 'codigo'
		]

	class Meta:
		model = Mensajeria_Externa


admin.site.register(Mensajeria_Externa, Admin_Mensajeria_Externa)



class AdminReporte(admin.ModelAdmin):
	list_display = ['id', 'permiso']
	ordering = ['permiso']

	class Meta:
		model = Reporte


admin.site.register(Reporte, AdminReporte)



class AdminSucursales(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'vlan', 'direccion']
	ordering = ['-id']

	class Meta:
		model = Sucursales


admin.site.register(Sucursales, AdminSucursales)


class AdminDepartamento(admin.ModelAdmin):
	list_display = ['id','departamento']
	ordering = ['-id']

	class Meta:
		model = Departamento


admin.site.register(Departamento, AdminDepartamento)


class AdminConfiguracion(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'habilitar']
	ordering = ['-id']

	class Meta:
		model = Configuracion


admin.site.register(Configuracion, AdminConfiguracion)
