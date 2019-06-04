from django.shortcuts import render

# Create your views here.
from Mensajeria.models import (
	Mensajeria_Externa, Mensajeria_Interna, Sucursales, Departamento,
	Reporte, Sucursales, Configuracion
)
from django.db.models import Q

from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import os
import io
import json
import time
import datetime
from datetime import datetime, date

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

import ldap
from projectMensajeria.settings import (
	URL, PASS_LDAP, CORREO, MEDIA_ROOT, MEDIA_URL, CARPETA_ACUSE,
	RUTA_CARPETA_ACUSE, RUTA_LOG, AD_LDAP_URL, DOMAIN
)

from ipware import get_client_ip

from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage

from Mensajeria.envio_de_correos import (
	enviar_correo_destinatario, enviar_correo_remitente,
	enviar_correo_acuse_externo
)

import logging


logging.config.dictConfig({
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'console': {
			'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
		},
		'file': {
			'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
		}
	},
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'console'
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'formatter': 'file',
			'filename': RUTA_LOG
		}
	},
	'loggers': {
		'': {
			'level': 'DEBUG',
			'handlers': ['console', 'file']
		},
		'django.request': {
			'level': 'DEBUG',
			'handlers': ['console', 'file']
		}
	}
})


def buscar_sucursal(request):
	ip = get_client_ip(request)[0]
	vlan = (
		'%s.%s.%s' % (
			ip.split('.')[0],
			ip.split('.')[1],
			ip.split('.')[2]
		)
	)
	return vlan


def configuraciones():
	configuracion = Configuracion.objects.all()

	return configuracion


"""
Terminado:
	Funcion para iniciar sesion
"""
def login(request):
	logger = logging.getLogger('Inicio de Sesión')

	mensaje = ''
	if request.method == 'POST':
		v_usuario = request.POST.get('username')
		v_clave = request.POST.get('password')

		try:
			l = ldap.initialize(AD_LDAP_URL)
			l.protocol_version = ldap.VERSION3
			l.simple_bind_s("%s@%s" % (v_usuario, DOMAIN), v_clave)
			l.unbind_s()
			usuario = auth.authenticate(username=v_usuario, password=PASS_LDAP)
			auth.login(request, usuario)

			logger.info('Sesión iniciada correctamente.')

			return redirect(mensajeria_personal)

		except ldap.INVALID_CREDENTIALS:
			mensaje = 'Usuario o clave incorrecto'
			logger.error(mensaje)
		except ldap.SERVER_DOWN:
			mensaje = 'No se pudo conectar con el servidor LDAP'
			logger.warning(mensaje)
	
	return render(request, 'login.html',
		{'mensaje': mensaje, 'video': (MEDIA_URL + 'video/ayuda.mp4')}
	)


"""
Terminado:
	Funcion para cerrar sesion
"""
@login_required(login_url='/login/')
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login")


@login_required(login_url='/login/')
@permission_required('Mensajeria.crear_reporte', raise_exception=True)
def reporte(request):

	if request.method == 'POST':
		fechaHasta = request.POST.get('fechaHasta')
		fechaDesde = request.POST.get('fechaDesde')
		descripcion = request.POST.get('descripcion')
		remitente = request.POST.get('remitente')
		destinatario = request.POST.get('destinatario')
	"""
	#Pendiente por convertir en formato '0,0,0'
		fechaHasta = str(fechaHasta).split('-')
		ini = [
			int(fechaHasta[0]),
			int(fechaHasta[1]),
			int(fechaHasta[2])
		]

		fechaDesde = str(fechaDesde).split('-')
		fin = str('%s%s%s'%(fechaDesde[0],fechaDesde[1],fechaDesde[2]))


		print('\n\n-----------',ini)
		print('-----------', type(ini))
		# print('-----------',date(ini))

	# mensajeria = Mensajeria_Interna.objects.all()
	# print('\n\n', 'Query 1', mensajeria[0].fecha_recibido, '\n\n')
	"""




	ini = date(2005, 9, 5)
	fin = date(2018, 9, 7)
	mensajeria = Mensajeria_Interna.objects.filter(
		fecha_recibido__range=(ini, fin)
		)
	print('\n', 'Query 2', mensajeria, '\n\n')



	# mensajeria = Mensajeria_Interna.objects.filter(
	# 	Q(fecha_recibido__gte=ini),
	# 	Q(fecha_recibido__lte=fin)
	# 	)
	# print('\n', 'Query 3', mensajeria, '\n\n')
	print(ini)
	print(fin)

	# mensajeria = Mensajeria_Interna.objects.get(
	# 		Q(fechaHasta__lte='Who'),
	# 		Q(fechaDesde__lte=date(2005, 5, 2)) |
	# 		Q(descripcion=descripcion),
	# 		Q(remitente=remitente),
	# 		Q(destinatario=destinatario)
	#     )

	contenido = {
		'mensajeria': mensajeria,
	}

	return render(request, 'reportes.html', contenido)

def estado_serializer(estado, fecha_entrega):
		return {
		'estado': str(estado),
		'fecha': str(fecha_entrega)
	}


"""
Terminado:
	Funcion para mostrar las mensajerias
	personal de cada usuario
"""
@login_required(login_url='/login/')
def mensajeria_personal(request):
	usuario = request.user.get_full_name()
	mensajeria = Mensajeria_Interna.objects.all()
	
	c_tot = 0
	c_rec = 0
	c_pen = 0
	c_env = 0

	for m in mensajeria:
		if m.estado == 'Recibido' and m.destinatario == usuario:
			c_rec += 1
			c_tot += 1
		elif m.estado == 'Pendiente' and m.destinatario == usuario:
			c_pen += 1
			c_tot += 1

		if m.remitente == usuario:
			c_env += 1

	datos = {
		'c_tot': c_tot,
		'c_rec': c_rec,
		'c_pen': c_pen,
		'c_env': c_env,
		'mensajeria': [],
		'clase1': '',
		'clase2': '',
		'clase3': '',
		'clase4': '',
		'mostrar_chat_de_ayuda': configuraciones()[0].habilitar,
		'video': (MEDIA_URL + 'video/ayuda.mp4')
	}
	
	if request.method == 'GET':
		estado = request.GET.get('estado', '')

		if estado:
			if estado=='todo':
				mensajeria = Mensajeria_Interna.objects.all().order_by(
					'-fecha_recibido').filter(destinatario=usuario).exclude(
					estado='Retenido').exclude(estado='En Transito')

				datos['clase1'] = 'black'
				for men in mensajeria:
					datos['mensajeria'].append(men)
				return render(request, 'mensajeriaPersonal.html', datos)

			elif estado == 'enviada':
				mensajeria = Mensajeria_Interna.objects.order_by(
					'-fecha_recibido').filter(remitente=usuario,
				).exclude(estado='Retenido')

				datos['clase2'] = 'black'
				for men in mensajeria:
					datos['mensajeria'].append(men)
				return render(request, 'mensajeriaPersonal.html', datos)

			else:
				mensajeria = Mensajeria_Interna.objects.filter(estado=estado,
				destinatario=usuario).order_by('-fecha_recibido')

				if estado == 'Pendiente':
					datos['clase3'] = 'black'
				elif estado == 'Recibido':
					datos['clase4'] = 'black'

				for men in mensajeria:
					datos['mensajeria'].append(men)
				return render(request, 'mensajeriaPersonal.html', datos)
		datos['clase3'] = 'black'

	mensajeria = Mensajeria_Interna.objects.filter(estado='Pendiente'
		).order_by('-fecha_recibido').filter(destinatario=usuario)

	for men in mensajeria:
		datos['mensajeria'].append(men)
	
	return render(request, 'mensajeriaPersonal.html', datos)


"""
Terminado:
	Funcion para registrar las Mensajerias Internas.
"""
@login_required(login_url='/login/')
@permission_required('Mensajeria.crear_mensajeria', raise_exception=True)
def registrar_mensajeria_interna(request):
	suc = Sucursales.objects.get(vlan=buscar_sucursal(request))

	id_departamento = Departamento.objects.all()
	mensajeria = Mensajeria_Interna.objects.all().order_by('-id')

	estado = 'Retenido'
	codigo = 0
	datos = {}
	remitente_externo = False
	if request.method == 'POST':
		recepcionista = request.user.id
		sucursal = request.POST.get('sucursal')
		remitente_externo = request.POST.get('remitente_externo')
		remitente = request.POST.get('remitente')
		destinatario = request.POST.get('destinatario')
		descripcion = request.POST.get('descripcion')
		observacion = request.POST.get('observacion')
		comentario = request.POST.get('comentario')
		prioridad = request.POST.get('prioridad')
		fechaRecibido = request.POST.get('fechaRecibido')
		horaRecibido = request.POST.get('horaRecibido')
		fecha_hora = ('%s %s:00.000000' % (fechaRecibido, horaRecibido))

		if not remitente_externo:
			remitente_externo = False
		elif remitente_externo == 'on':
			remitente_externo = True

		if not observacion:
			observacion = 'Sin observacion'
		if not comentario:
			comentario = 'Sin comentario'

		try:
			codigo = Mensajeria_Interna.objects.latest('id')
			codigo = codigo.id
		except:
			codigo = 0
		codigo += 1
		codigo = ('MEN-INT-%s-%s' %
			(datetime.now().strftime("%d%m%Y"), codigo)
		)

		guardar = Mensajeria_Interna.objects.create(
			recepcionista_id = recepcionista,
			sucursal = sucursal,
			remitente_externo = remitente_externo,
			remitente = remitente,
			destinatario = destinatario,
			descripcion = descripcion,
			fecha_recibido = fecha_hora,
			observacion = observacion,
			comentario = comentario,
			prioridad = prioridad,
			estado = estado,
			codigo = codigo
		)

		return redirect(registrar_mensajeria_interna)

	lista_mensajeria = []
	for m in mensajeria:
		men = {
			'id': m.id,
			'codigo': m.codigo,
			'remitente_externo': m.remitente_externo,
			'remitente': m.remitente,
			'destinatario': m.destinatario,
			'descripcion': m.descripcion,
			'fecha_recibido': m.fecha_recibido,
			'estado': m.estado,
			'boton': (asignar_primer_estado(
					m.remitente_externo, m.id, m.estado, request.user,
					m.recepcionista, m.sucursal, suc.nombre
				)
			),
		}
		lista_mensajeria.append(men)

	datos = {
		'mensajeria': lista_mensajeria,
		'usuariofull': request.user.get_full_name(),
		'departamento': id_departamento,
	}

	return render(request, 'mensajeriaInterna.html', datos)


"""
Terminado:
	Funcion para registrar las Mensajerias Externas,
	y cerrar las Mensajerias que estan en Transito.
"""
@login_required(login_url='/login/')
@permission_required('Mensajeria.crear_mensajeria', raise_exception=True)
def registrar_mensajeria_externa(request):
	mensajeria = Mensajeria_Externa.objects.all().order_by('-id')
	usuario = request.user.get_full_name()

	c_tot = 0
	c_rec = 0
	c_pen = 0
	c_env = 0

	estado = 'Pendiente'
	codigo = 0
	datos = {}

	if request.method == 'POST':
		tipo = request.POST.get('tipo')

		if tipo == 'registrar':
			recepcionista = request.user.id
			sucursal = request.POST.get('sucursal')

			try:
				codigo = Mensajeria_Externa.objects.latest('id')
				codigo = codigo.id
			except:
				codigo = 0
			codigo += 1
			codigo = ('MEN-EXT-%s-%s' % (datetime.now().strftime("%d%m%Y"), codigo))

			mensajero = request.POST.get('mensajero')
			fecha_envio_depto = request.POST.get('fecha_envio_depto')
			hora_envio_depto = request.POST.get('hora_envio_depto')
			departamento = request.POST.get('departamento')
			encargado = request.POST.get('encargado')
			entregado_por = request.POST.get('entregado_por')
			descripcion = request.POST.get('descripcion')
			destinatario = request.POST.get('destinatario')
			prioridad = request.POST.get('prioridad')

			guardar = Mensajeria_Externa.objects.create(
				sucursal = sucursal,
				recepcionista_id = recepcionista,
				codigo = codigo,
				mensajero = mensajero,

				fecha_envio_depto = fecha_envio_depto,
				hora_envio_depto = hora_envio_depto,
				departamento_id = departamento,
				encargado = encargado,
				entregado_por = entregado_por,

				descripcion = descripcion,
				destinatario = destinatario,
				prioridad = prioridad,
				estado = 'En Transito',

				hora_salida=time.strftime("%I:%M"),
			)
			return redirect(registrar_mensajeria_externa)

		elif tipo == 'cerrar':
			hora_entrada = request.POST.get('hora_entrada')
			acuse = request.POST.get('acuse')
			comentario = request.POST.get('comentario')
			codigo = request.POST.get('codigo')

			actualizar = Mensajeria_Externa.objects.get(codigo = codigo)
			try:
				if request.FILES['archivo']:
					archivo = request.FILES['archivo']
					fs = FileSystemStorage(location=MEDIA_ROOT+'acuse')
					filename = fs.save(archivo.name, archivo)

					actualizar.archivo_acuses = filename

			except Exception as ex:
				print('\n**********\n', ex, '\n**********\n')

			actualizar.hora_entrada = hora_entrada
			actualizar.acuse = acuse
			actualizar.comentario = comentario
			actualizar.estado = 'Enviado'
			actualizar.save()

			usuario = User.objects.get(
				first_name=actualizar.entregado_por.split()[0],
				last_name=actualizar.entregado_por.split()[1]
			)
			correo_dest = usuario.email

			enviar_correo_acuse_externo(
				actualizar.entregado_por, actualizar.destinatario,
				actualizar.codigo, correo_dest,
			)

			return redirect(registrar_mensajeria_externa)

	datos = {
		'c_tot': c_tot,
		'c_rec': c_rec,
		'c_pen': c_pen,
		'c_env': c_env,
		'mensajeria': mensajeria
	}

	return render(request, 'mensajeriaExterna.html', datos)


"""
Terminado:
	Funcion para asignarle los estados a las mensajerias
	y los colores a los botones, al momento de recargar
	la pagina.
"""
def asignar_primer_estado(
	remitente_externo, id_mensajeria, estado, usuario_act, historial,
	sucursal, sucursal_act):

	btn = {
		'clase': '',
		'texto': '',
		'valor': '',
		'modal': '',
	}

	if estado == 'Retenido':
		if remitente_externo == False:
			if sucursal_act == sucursal:
				btn['clase'] = 'enviar btn control ancho waves-effect waves-light'
				btn['texto'] = 'Enviar'
				btn['valor'] = '%s-%s' % (id_mensajeria, 'Retenido')
			else:
				btn['clase'] = ("""disabled btn control ancho waves-effect
				waves-light """)
				btn['texto'] = 'Enviar'
				btn['valor'] = '%s-%s' % (id_mensajeria, 'Retenido')
		else:
			btn['clase'] = 'enviar btn control ancho waves-effect waves-light'
			btn['texto'] = 'Enviar'
			btn['valor'] = '%s-%s' % (id_mensajeria, 'Retenido')


	elif estado == 'En_Transito' or estado == 'En Transito':
		if remitente_externo == False:
			if usuario_act == historial or sucursal_act == sucursal:
				btn['clase'] = ("""disabled btn control ancho waves-effect
				waves-light yellow accent-4 black-text""")
				btn['texto'] = 'Recibir'
				btn['valor'] = "%s-En_Transito" % (id_mensajeria)
			else:
				btn['clase'] = ("""recibir btn control ancho waves-effect
				waves-light yellow accent-4 black-text""")
				btn['texto'] = 'Recibir'
				btn['valor'] = "%s-En_Transito" % (id_mensajeria)
		else:
			btn['clase'] = ("""recibir btn control ancho waves-effect
			waves-light yellow accent-4 black-text""")
			btn['texto'] = 'Recibir'
			btn['valor'] = "%s-En_Transito" % (id_mensajeria)

	elif estado == 'Pendiente':
		if remitente_externo == False:
			if usuario_act == historial:
				btn['clase'] = ("""disabled btn ancho waves-effect waves-light
				green accent-4 modal-trigger""")
				btn['texto'] = 'Entregar'
				btn['valor'] = '%s-%s' % (id_mensajeria, 'Pendiente')
			else:
				btn['clase'] = ("""entregar btn ancho waves-effect waves-light
				green accent-4 modal-trigger""")
				btn['texto'] = 'Entregar'
				btn['sin_modal'] = "data-target=firma"
				btn['modal'] = "firma"
				btn['valor'] = '%s-%s' % (id_mensajeria, 'Pendiente')
		else:
			btn['clase'] = ("""entregar btn ancho waves-effect waves-light
			green accent-4 modal-trigger""")
			btn['texto'] = 'Entregar'
			btn['sin_modal'] = "data-target=firma"
			btn['modal'] = "firma"
			btn['valor'] = '%s-%s' % (id_mensajeria, 'Pendiente')

	elif estado == 'Recibido':
		btn['clase'] = 'disabled act btn control ancho'
		btn['texto'] = 'Entregar'
		btn['valor'] = ''

	return btn


"""
Terminado:
	Funcion para validar los estados a las mensajerias,
	y así poder asignarle un nuevo estado y nuevos
	colores a los botones, al momento de hacer click
	a un boton, ya sea, Enviar, Recibir o Entregar.
"""
def validar_estados(
	id_mensajeria, estado, usuario_act, historial, sucursal, sucursal_act,
	remitente_externo):

	btn = {
		'clase': '',
		'texto': '',
		'valor': '',
		'modal': '',
	}

	if estado == 'Retenido':
		if remitente_externo == 'False':
			if usuario_act == historial or sucursal == sucursal_act:
				btn['clase'] = ("""disabled btn control ancho waves-effect
				waves-light yellow accent-4 black-text""")
				btn['texto'] = 'Recibir'
				btn['valor'] = "%s-En_Transito" % (id_mensajeria)
			else:
				btn['clase'] = ("""recibir btn control ancho waves-effect
				waves-light yellow accent-4 black-text""")
				btn['texto'] = 'Recibir'
				btn['valor'] = "%s-En_Transito" % (id_mensajeria)
		else:
			btn['clase'] = ("""recibir btn control ancho waves-effect
			waves-light yellow accent-4 black-text""")
			btn['texto'] = 'Recibir'
			btn['valor'] = "%s-En_Transito" % (id_mensajeria)

	elif estado == 'En_Transito' or estado == 'En Transito':
		if usuario_act == historial:
			btn['clase'] = ("""disabled btn ancho waves-effect waves-light
			green accent-4 modal-trigger""")
			btn['texto'] = 'Entregar'
			btn['valor'] = "%s-%s" % (id_mensajeria, 'Pendiente')
		else:
			btn['clase'] = ("""entregar btn ancho waves-effect waves-light
			green accent-4 modal-trigger""")
			btn['texto'] = 'Entregar'
			btn['modal'] = "firma"
			btn['valor'] = "%s-Pendiente" % (id_mensajeria)

	elif estado == 'Pendiente':
		if usuario_act == historial:
			btn['clase'] = ("""disabled btn control ancho waves-effect
			waves-light green accent-4 modal-trigger""")
			btn['texto'] = 'Recibido'
		else:
			btn['clase'] = ("""disabled btn control ancho""")
			btn['texto'] = 'Recibido'
			btn['valor'] = ''

	return btn


# ***********************************************************************#
# <-------------------------- Funsiones AJAX --------------------------> #
# ***********************************************************************#

"""
Terminado:
	Funcion para marcar las mensajerias interna como entregada,
	y enviar correo al remitente, avisando que ya el
	destinatario recibio la mensajeria
"""
def entregar_mensajeria_ajax(request):
	fecha = datetime.now()
	pasos = []
	mensaje = ''
	suc = Sucursales.objects.get(vlan=buscar_sucursal(request))
	r_ext = request.POST.get('r_ext')

	if request.method == 'POST':
		id_mensajeria = request.POST.get('id_mensajeria')
		tercero = request.POST.get('tercero')
		estado = request.POST.get('estado')
		r_ext = request.POST.get('r_ext')

		nuevo_estado = 'Recibido'
		mensajeria_In = Mensajeria_Interna.objects.get(id=id_mensajeria)

		btn = validar_estados(
			id_mensajeria, estado, request.user,
			mensajeria_In.hist_enviado_por, mensajeria_In.sucursal, suc, r_ext
		)

		if not tercero:
			tercero = mensajeria_In.destinatario

		mensajeria_In.estado = nuevo_estado
		mensajeria_In.fecha_entrega = fecha
		mensajeria_In.recibido_por = tercero
		mensajeria_In.hist_entregado_por = request.user.get_full_name()
		mensajeria_In.save()

		if not r_ext:
			r_ext = False
		elif r_ext == 'on':
			r_ext = True

		if r_ext == 'False':
			nuevo_estado = [estado_serializer(
					mensajeria_In.estado, mensajeria_In.fecha_entrega
				)
			]

			usuario = User.objects.get(
				first_name=mensajeria_In.remitente.split()[0],
				last_name=mensajeria_In.remitente.split()[1]
			)
			correo_remi = usuario.email
			
			mensaje = enviar_correo_remitente(
				mensajeria_In.remitente, mensajeria_In.codigo,
				tercero, mensajeria_In.sucursal, correo_remi
			)

		else:
			mensaje = 'La mensajeria ha sido marcada como entregada.'

		return HttpResponse(
			json.dumps({
				'estado': nuevo_estado,
				'mensaje': mensaje,
				'boton': btn
			}),
			content_type="application/json"
		)


"""
Terminado:
	Funcion para cargar datos al modal para
	mostrar	detalles de la Mensajeria Interna
"""
def detalles_mensajeria_interna_ajax(request):
	datos = {
		'codigo' : '',
		'comentario' : '',
		'fecha_entrega' : '',
		'prioridad' : '',
		'observacion' : '',
		'recepcionista' : '',
		'recibido_por' : '',
		'sucursal' : '',
		'mensaje' : '',
		'tipo_remitente': '',
	}

	if request.method == 'POST':
		codigo = request.POST.get('codigo')

		try:
			m = Mensajeria_Interna.objects.get(codigo=codigo)

			if m.recibido_por == None:
				datos['recibido_por'] = 'Pendiente por entregar'
			else:
				datos['recibido_por'] = str(m.recibido_por)

			if m.fecha_entrega == None:
				datos['fecha_entrega'] = 'Pendiente por entregar'
			else:
				datos['fecha_entrega'] = str(m.fecha_entrega)

			datos['codigo'] = str(m.codigo)
			datos['comentario'] = str(m.comentario)
			datos['prioridad'] = str(m.prioridad)
			datos['observacion'] = str(m.observacion)
			datos['recepcionista'] = str(m.recepcionista.get_full_name())
			datos['sucursal'] = str(m.sucursal)
			datos['tipo_remitente'] = str(m.remitente_externo)
		except Exception as e:
			print('Se ha producido un error: %s' %e)
			datos['mensaje'] = 'Se ha producido un error'

	return HttpResponse(
		json.dumps(datos),
		content_type="application/json"
	)


"""
Terminado:
	Funcion para cargar datos al modal para
	mostrar	detalles de la Mensajeria Externa
"""
def detalles_mensajeria_externa_ajax(request):
	datos = {
		'codigo' : '',
		'recepcionista' : '',
		'mensajero' : '',
		'acuse' : '',
		'comentario' : '',
		'prioridad' : '',
		'sucursal' : '',
		'departamento' : '',
		'encargado' : '',
		'hora_salida' : '',
		'hora_entrada' : '',
		'mensaje' : '',
		'estado': '',
		'archivo': '',
	}

	if request.method == 'POST':
		codigo = request.POST.get('codigo')

		m = Mensajeria_Externa.objects.get(codigo=codigo)
		try:
			datos['codigo'] = str(m.codigo)
			datos['recepcionista'] = str(m.recepcionista.get_full_name())
			datos['mensajero'] = str(m.mensajero)
			datos['acuse'] = str(m.acuse)
			datos['comentario'] = str(m.comentario)
			datos['prioridad'] = str(m.prioridad)
			datos['sucursal'] = str(m.sucursal)
			datos['departamento'] = str(m.departamento)
			datos['encargado'] = str(m.encargado)
			datos['hora_salida'] = str(m.hora_salida)
			datos['hora_entrada'] = str(m.hora_entrada)
			datos['estado'] = str(m.estado)
			datos['archivo'] = str(
				(RUTA_CARPETA_ACUSE + str(m.archivo_acuses))
			)

		except Exception as e:
			datos['mensaje'] = ('Se ha producido un error: ', e)

	return HttpResponse(
		json.dumps(datos),
		content_type="application/json"
	)


"""
Terminado:
	Funcion para cargar los nombres de los
	departamentos, para el auto completado
"""
def cargar_departamentos_ajax(request):
	departamento = Departamento.objects.all()
	dep = {}
	dep_con_id = {}

	for departamento in departamento:
		dep[departamento.departamento] = ''
		dep_con_id[departamento.departamento] = departamento.id

	return HttpResponse(
		json.dumps({
			'dep': dep,
			'dep_con_id': dep_con_id,
		}),
		content_type="application/json"
	)


"""
Terminado:
	Funcion para cargar los nombres de los
	usuarios, para el auto completado
"""
def cargar_usuarios_ajax(request):
	usuario = User.objects.all()
	usuarios = {}

	for usuario in usuario:
		usuarios[usuario.get_full_name()] = ''

	return HttpResponse(
		json.dumps({
			'usuarios': usuarios,
		}),
		content_type="application/json"
	)


"""
Terminado:
	Funcion para cambiar los estados a las mensajerias
	y los colores a los botones, al momento de hacer
	click a un boton, ya sea, Enviar, Recibir o Entregar.
"""
def cambiar_estado_ajax(request):
	suc = Sucursales.objects.get(vlan=buscar_sucursal(request))

	fecha = datetime.now()
	datos = {
		'mensaje': '',
		'estado': '',
		'boton': '',
		'clase': ''
	}

	if request.method == 'POST':
		id_mensajeria = request.POST.get('id_mensajeria')
		estado = request.POST.get('estado')
		r_ext = request.POST.get('r_ext')

		if estado == 'En_Transito':
			mensajeria_In = Mensajeria_Interna.objects.get(id=id_mensajeria)

			datos['estado'] = 'Pendiente'
			datos['clase'] = 'estado red accent-4'
			datos['boton'] = validar_estados(
				id_mensajeria, estado, request.user,
				mensajeria_In.hist_enviado_por, mensajeria_In.sucursal,
				suc.nombre, mensajeria_In.remitente_externo
			)

			mensajeria_In.fecha_enviado = fecha
			mensajeria_In.estado = datos['estado']
			mensajeria_In.hist_recibido_por = request.user.get_full_name()
			mensajeria_In.save()
			datos['mensaje'] = 'Mensajeria recibida'

			""" * * * Enviar correo al destinatario * * * """			
			usuario = User.objects.get(
				first_name=mensajeria_In.destinatario.split()[0],
				last_name=mensajeria_In.destinatario.split()[1]
			)
			correo_dest = usuario.email

			enviar_correo_destinatario(
				mensajeria_In.destinatario, mensajeria_In.codigo,
				mensajeria_In.remitente, suc, correo_dest
			)

		elif estado == 'Retenido':
			mensajeria_In = Mensajeria_Interna.objects.get(id=id_mensajeria)
			recepcionista = str(mensajeria_In.recepcionista)
			sucursal = str(mensajeria_In.sucursal)

			datos['estado'] = 'En Transito'
			datos['clase'] = 'estado yellow accent-4 black-text'
			datos['boton'] = validar_estados(
				id_mensajeria, estado, request.user,
				recepcionista, sucursal, suc.nombre, r_ext
			)

			mensajeria_In.fecha_enviado = fecha
			mensajeria_In.estado = datos['estado']
			mensajeria_In.hist_enviado_por = request.user.get_full_name()
			mensajeria_In.save()
			datos['mensaje'] = 'La mensajeria ha sido enviada'

	return HttpResponse(
		json.dumps(
			datos
		),
		content_type="application/json"
	)


"""Listo"""
@login_required(login_url='/login/')
def prueba(request):
	id_departamento = Departamento.objects.all()
	mensajeria = Mensajeria_Interna.objects.all().order_by('-id')

	lista_mensajeria=[]
	for m in mensajeria:
		men = {
			'id': m.id,
			'codigo': m.codigo,
			'remitente': m.remitente,
			'destinatario': m.destinatario,
			'descripcion': m.descripcion,
			'fecha_recibido': m.fecha_recibido,
			'estado': m.estado,
			'boton': asignar_primer_estado(
				m.id, m.estado, request.user, m.recepcionista,
				m.sucursal, sucursal.nombre),
		}
		lista_mensajeria.append(men)
		print('**********************\nBOTON', men['id'], men['boton'])

	datos = {
		'mensajeria': lista_mensajeria,
		'usuariofull': request.user.get_full_name(),
		'departamento': id_departamento,
	}
	return render(request, 'asd.html', datos)
