from django.db import models

# Create your models here.
from datetime import date, time
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from projectMensajeria.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage

ruta_archivos = FileSystemStorage(location=MEDIA_ROOT + 'acuse/')

TIPO_PRIORIDAD_EXT = (
	('Baja', 'Baja'),
	('Media', 'Media'),
	('Alta', 'Alta'),
)

TIPO_PRIORIDAD_INT = (
	('Baja', 'Baja'),
	('Alta', 'Alta'),
)

ESTADO_MENSAJERIA_INT = (
	('Recibido', 'Recibido'),
	('Pendiente', 'Pendiente'),
	('En Transito', 'En Transito'),
	('Retenido', 'Retenido'),
)

ESTADO_MENSAJERIA_EXT = (
	('En Transito', 'En Transito'),
	('Enviado', 'Enviado'),
)
NOMBRE_MOSTRAR_CHAT_DE_AYUDA = (
	('habilitar_mostrar_ayuda', 'Habilitar Mostrar Ayuda'),
	('mostrar_ayuda', 'Mostrar Ayuda')
)

class Departamento(models.Model):
	departamento = models.CharField(max_length=30, blank=False, null=False)

	def __str__(self):
		return self.departamento


class Mensajeria_Interna(models.Model):
	codigo = models.CharField(_("Codigo de Mensajeria"),
	max_length=30, blank=False, null=False)
	recepcionista = models.ForeignKey(
		User, on_delete=models.SET_NULL, blank=True, null=True)
	sucursal = models.CharField(max_length=30, blank=False, null=False)
	remitente_externo = models.BooleanField(default=False)
	remitente = models.CharField(max_length=30, blank=False, null=False)
	destinatario = models.CharField(max_length=30, blank=False, null=False)
	recibido_por = models.CharField(max_length=30, blank=True, null=True)
	descripcion = models.CharField(max_length=200, blank=False, null=False)
	fecha_recibido = models.DateTimeField(
		_("Fecha Recibido"), editable=True, blank=False, null=False)
	fecha_enviado = models.DateTimeField(
		_("Fecha Enviado"), editable=True, blank=True, null=True)
	fecha_recibido_int = models.DateTimeField(
		_("Fecha Recibido en Recp."), editable=True, blank=True, null=True)
	fecha_entrega = models.DateTimeField(
		_("Fecha Entregado"), editable=True, blank=True, null=True)
	comentario = models.CharField(max_length=200, blank=True, null=True)
	observacion = models.CharField(max_length=200, blank=True, null=True)
	prioridad = models.CharField(
		max_length=5, blank=False, null=False, choices=TIPO_PRIORIDAD_INT)
	estado = models.CharField(
		max_length=15, blank=False, null=False, choices=ESTADO_MENSAJERIA_INT)
	hist_enviado_por = models.CharField(_("Historial Enviado por"),
		max_length=30, blank=True, null=True)
	hist_recibido_por = models.CharField(_("Historial Recibido por"),
		max_length=30, blank=True, null=True)
	hist_entregado_por = models.CharField(_("Historial Entregado por"),
		max_length=30, blank=True, null=True)

	def __str__(self):
		return self.codigo


class Mensajeria_Externa(models.Model):
	#--- INFORMACION GENERAR ---
	sucursal = models.CharField(max_length=30, blank=False, null=False)
	recepcionista = models.ForeignKey(
		User, on_delete=models.SET_NULL, blank=True, null=True)
	codigo = models.CharField(
		_("Codigo de Mensajeria"),max_length=30, blank=False, null=False)
	mensajero = models.CharField(
		_("Nombre Mensajero"), max_length=30, blank=False, null=False)

	#--- INFORMACIÓN DEL DEPARTAMENTO QUE ENVÍA LA CORRESPONDENCIA ---
	fecha_envio_depto = models.DateField(
		_("Fecha Enviado Depto."), editable=True, blank=False, null=False)
	hora_envio_depto = models.TimeField(
		_("Hora Enviado Depto."), editable=True, blank=False, null=False)
	departamento = models.ForeignKey(
		'Departamento', on_delete=models.SET_NULL, blank=True, null=True)
	encargado = models.CharField(
		_("Encargado del Departamento"), max_length=30, blank=False, null=False)
	entregado_por = models.CharField(
		_("Quien Entrega"), max_length=30, blank=False, null=False)

	#--- DETALLES DE LA CORRESPONDENCIA ---
	descripcion = models.CharField(max_length=200, blank=False, null=False)
	destinatario = models.CharField(max_length=100, blank=False, null=False)
	prioridad = models.CharField(
		max_length=5, blank=False, null=False, choices=TIPO_PRIORIDAD_EXT)

	#--- DETALLES DE ENTREGA/RECEPCIÓN DE CORRESPONDENCIA ---
	hora_salida = models.TimeField(
		_("Hora Salida Mensajero"), editable=True, blank=True, null=True)
	hora_entrada = models.TimeField(
		_("Hora Entrada Mensajero"), editable=True, blank=True, null=True)
	acuse = models.CharField(max_length=200, blank=True, null=True)
	comentario = models.CharField(max_length=200, blank=True, null=True)
	estado = models.CharField(
		max_length=15, blank=False, null=False, choices=ESTADO_MENSAJERIA_EXT)
	archivo_acuses = models.FileField(upload_to = ruta_archivos)
	def __str__(self):
		return self.codigo


class Reporte(models.Model):
	permiso = models.ForeignKey(
		User, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.permiso


class Sucursales(models.Model):
	nombre = models.CharField(max_length=30, blank=False, null=False)
	direccion = models.CharField(max_length=150, blank=False, null=False)
	vlan = models.CharField(max_length=30, blank=False, null=False)

	def __str__(self):
		return self.nombre


class Permiso(models.Model):

	class Meta:
		permissions = (
		("ver", "Puede ver"),
		("crear_mensajeria", "Puede crear mensajeria"),
		("crear_reporte", "Puede crear reporte"),
		("eliminar", "Puede Eliminar"),
	)


class Configuracion(models.Model):

	nombre = models.CharField(max_length=25, blank=False, null=False)
	habilitar = models.BooleanField(default=False)
	def __str__(self):
		return self.nombre


"""
INFORMACION GENERAR
-----------------------------------------------------------------
	*sucursal
	*recepcionista
	*codigo
	*mensajero


INFORMACIÓN DEL DEPARTAMENTO QUE ENVÍA LA CORRESPONDENCIA
-----------------------------------------------------------------
	*fecha_envio_depto
	*hora_envio_depto
	*departamento
	*encargado
	*entregado_por

	FECHA
	HORA
	DEP. REMITENTE (Departamento que envía la doc.)
	ENCARGADO (Persona que dirige el Departamento)
	ENTREGADO POR (Persona que entrega la Correspondencia)


DETALLES DE LA CORRESPONDENCIA
-----------------------------------------------------------------
	*descripcion
	*destinatario
	*prioridad

	destinatario (a quien va dirigido)
	prioridad


DETALLES DE ENTREGA/RECEPCIÓN DE CORRESPONDENCIA
-----------------------------------------------------------------
	*hora_salida
	*hora_entrada
	*acuse
	*comentario

	hora salida (envío)
	hora entrada (entrega)
	acuse de recibo
	comentarios adicionales
	firma del mensajero o persona que entregó

TODS LOS CAMPOS
-----------------------------------------------------------------

	sucursal
	recepcionista
	codigo
	mensajero
	fecha_envio_depto
	hora_envio_depto
	departamento
	encargado
	entregado_por
	descripcion
	destinatario
	prioridad
	hora_salida
	hora_entrada
	acuse
	comentario

"""
