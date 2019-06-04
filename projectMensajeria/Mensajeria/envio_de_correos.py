from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from projectMensajeria.settings import URL, CORREO, RUTA_LOG, BASE_DIR
import logging
from datetime import datetime


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


def enviar_correo_destinatario(
	destinatario, codigo, remitente, sucursal, correo_dest):
	"""
	Funcion para enviar correo a los destinatarios,  
	notificando que tiene mensajerias pendientes, en recepcion.  
	"""

	logger = logging.getLogger('enviar_correo_destinatario')

	pasos = []
	correo_enviado = ('Mensajeria enviada a %s, con el codigo %s\n\n' %
		(destinatario, codigo))

	pasos.append(
		'\n%s\n*****************************************************************\n'
		% datetime.today().strftime("%d-%m-%Y %I:%M:%S %p")
	)

	try:
		pasos.append(
			'Paso 1 --->	Seleccionar el destinatario para enviar el correo.\n'
		)
		if not correo_dest:
			logger.warning('Mensajeria enviada a %s, con el codigo %s, pero el destinatario no tiene email.'
				% (destinatario, codigo)
			)
			pasos.append('			Mensajeria enviada a % s, con el codigo % s, pero el destinatario no tiene email.'
				% (destinatario, codigo)
			)
		else:
			pasos.append('			Listo\n')

			pasos.append('Paso 2 --->	Enviar el correo.\n')

			html_content = ("""
				<style>
					body {
						background-color: #fff;
						color: rgb(85, 87, 93):
					}
					.padding{
						padding-top: 0px;
						margin: 15px auto;
						width: 600px;
					}
					.felicidad {
						color: #0071bd;
						font-size: 46px
					}
					h3 {
						font-size: 20px
					}
					.color {
						color: blue;
						font-size: 24px;
						padding-bottom: 0px;
					}
					.usuario {
						margin-bottom: 0px;
						padding-bottom: 0px;
						font-size: 20px
					}
					a {
						font-size: 16px
					}
					img {
						margin: 0px;
						padding: 0px;
						width: 100%%;
					}
					a {
						color: #0071bc;
					}
					#a {
						text-decoration: none;
						color: #fff;
						background-color: #2b2d2d;
						text-align: center;
						letter-spacing: .5px;
						-webkit-transition: background-color .2s ease-out;
						transition: background-color .2s ease-out;
						cursor: pointer;
						border: none;
						border-radius: 5px;
						display: inline-block;
						height: 36px;
						line-height: 36px;
						padding: 0 16px;
						text-transform: uppercase;
						vertical-align: middle;
						-webkit-tap-highlight-color: transparent;
					}
					#a:hover {
						color: #a9a9a9;
						text-decoration: none;
					}
					p {
						text-align: left;
						margin: 15px 30px;
					}
					.center{
						text-align: center;
					}
				</style>

				<div class="center padding">
					<div>
						<div>
							<img src="%s/static/media/image/correo/banner-pendiente.png">
							<br>
							<p>Saludos, <strong>%s</strong>!</p>
							<p>Has recibido <strong>1</strong> correspondencia</p>
							<p>Código: <strong>%s</strong></p>
							<p>Enviado por: <strong>%s</strong></p>
							<p>Recepción: <strong>%s</strong></p>
							<br>
							<p>Tienes que pasar a retirarla por la recepción.</p>
							<br>
							<p> Tambien puedes acceder a la Aplicación a través de <a href="http://apps.bellbank.com">Apps Bellbank</a></p>
						</div>
						<br>
						<div class="center padding">
							<a id="a" href="%s" >Ver Correspondencia</a>
						</div>
					</div>
				</div>
			"""% (URL, destinatario, codigo, remitente, sucursal, URL))

			subject, from_email, to = ('Mensajeria Pendiente, Código '
				+ codigo, CORREO, correo_dest
			)

			text_content = 'Sistema de Mensajeria'
			msg = EmailMultiAlternatives(
				subject, text_content, from_email, [to]
			)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			pasos.append('			Listo\n')
			pasos.append('Paso 3 --->	Completado con exito.\n')
			pasos.append('			Listo\n')
			pasos.append(correo_enviado)
			logger.info(correo_enviado)

	except Exception as exepcion:
		pasos.insert(0,
				('\n\n%s --> ERROR:\n*************************************\n%s'
				% (datetime.today().strftime("%d-%m-%Y %I:%M:%S %p", exepcion))
			)
		)
		logger.warning(exepcion)

	finally:
		with open(
			BASE_DIR + '/log/correos_enviados.txt', 'a+') as archivo:
			for p in pasos:
				archivo.writelines(p)

		print('****** FIN *******')


def enviar_correo_remitente(
	remitente, codigo, tercero, sucursal, correo_remi):
	"""
	Funcion para enviar correo a los remitentes,  
	notificando que la mensajerias enviada  
	ya fue recibida por destinatario.  
	"""

	try:
		html_content = ("""
			<style>
				body {
					background-color: #fff;
					color: rgb(85, 87, 93):
				}
				.padding {
					padding-top: 0px;
					margin: 15px auto;
					width: 600px;
				}
				.felicidad {
					color: #0071bd;
					font-size: 46px
				}
				h3 {
					font-size: 20px
				}
				.color {
					color: blue;
					font-size: 24px;
					padding-bottom: 0px;
				}
				.usuario {
					margin-bottom: 0px;
					padding-bottom: 0px;
					font-size: 20px
				}
				a {
					font-size: 16px
				}
				img {
					margin: 0px;
					padding: 0px;
					width: 100%%;
				}
				a {
					color: #0071bc;
				}
				#a {
					text-decoration: none;
					color: #fff;
					background-color: #2b2d2d;
					text-align: center;
					letter-spacing: .5px;
					-webkit-transition: background-color .2s ease-out;
					transition: background-color .2s ease-out;
					cursor: pointer;
					border: none;
					border-radius: 5px;
					display: inline-block;
					height: 36px;
					line-height: 36px;
					padding: 0 16px;
					text-transform: uppercase;
					vertical-align: middle;
					-webkit-tap-highlight-color: transparent;
				}
				#a:hover {
					color: #a9a9a9;
					text-decoration: none;
				}
				p {
					text-align: left;
					margin: 15px 30px;
				}
				.center{
					text-align: center;
				}
			</style>

			<div class="center padding">
				<div>
					<div>
						<img src="%s/static/media/image/correo/banner-recibida.jpg">
						<br>
						<p>Saludos, <strong>%s</strong>!</p>
						<p>Su correspondencia <strong>%s</strong>, ha sido entregada satisfactoriamente.</p>
						<p>Recibida por: <strong>%s</strong></p>
						<p>Recepción: <strong>%s</strong></p>
						<br>
						<br>
						<p> Tambien puedes acceder a la Aplicación a través de <a href="http://apps.bellbank.com">Apps Bellbank</a></p>
					</div>
					<br>
					<div class="center padding">
						<a id="a" href="%s" >Ver Correspondencia</a>
					</div>
				</div>
			</div>""" %(URL, remitente, codigo, tercero, sucursal, URL)
		)

		subject, from_email, to = ('Mensajeria Entregada, Código '
		+ codigo, CORREO, correo_remi)

		text_content = 'Sistema de Mensajeria'
		msg = EmailMultiAlternatives(
			subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		mensaje = 'La mensajeria ha sido marcada como entregada.'
	except BadHeaderError:
		mensaje = 'No se pudo enviar el correo.'

	return mensaje


def enviar_correo_acuse_externo(
	remitente, destinatario, codigo, correo_remi):
	"""
	Funcion para enviar correo a los remitentes,  
	notificando que la mensajerias enviada  
	fuera de la institucion, ya fue entregada,  
	y que pase a buscar el acuse de recibo por recepcion.  
	"""

	try:
		html_content = ("""
			<style>
				body {
					background-color: #fff;
					color: rgb(85, 87, 93):
				}
				.padding {
					padding-top: 0px;
					margin: 15px auto;
					width: 600px;
				}
				.felicidad {
					color: #0071bd;
					font-size: 46px
				}
				h3 {
					font-size: 20px
				}
				.color {
					color: blue;
					font-size: 24px;
					padding-bottom: 0px;
				}
				.usuario {
					margin-bottom: 0px;
					padding-bottom: 0px;
					font-size: 20px
				}
				a {
					font-size: 16px
				}
				img {
					margin: 0px;
					padding: 0px;
					width: 100%%;
				}
				a {
					color: #0071bc;
				}
				#a {
					text-decoration: none;
					color: #fff;
					background-color: #2b2d2d;
					text-align: center;
					letter-spacing: .5px;
					-webkit-transition: background-color .2s ease-out;
					transition: background-color .2s ease-out;
					cursor: pointer;
					border: none;
					border-radius: 5px;
					display: inline-block;
					height: 36px;
					line-height: 36px;
					padding: 0 16px;
					text-transform: uppercase;
					vertical-align: middle;
					-webkit-tap-highlight-color: transparent;
				}
				#a:hover {
					color: #a9a9a9;
					text-decoration: none;
				}
				p {
					text-align: left;
					margin: 15px 30px;
				}
				.center{
					text-align: center;
				}
			</style>
			<div class="center padding">
				<div>
					<div>
						<img src="%s/static/media/image/correo/banner-acuse.png">
						<br>
						<br>
						<p>Saludos, <strong>%s</strong>!</p>
						<br>
						<p>Su correspondencia <strong>%s</strong>, enviada a <strong>%s</strong>, ha sido entregada.</p>
						<br>
						<p>Por favor, pasar por recepción a buscar su acuse de recibo</p>
						<br>
						<br>
						<p> Tambien puedes acceder a la Aplicación a través de <a href="http://apps.bellbank.com">Apps Bellbank</a></p>
					</div>
					<br>
					<div class="center padding">
						<a id="a" href="%s" >Ver Correspondencia</a>
					</div>
				</div>
			</div>""" % (URL, remitente, codigo, destinatario, URL)
		)

		subject, from_email, to = ('Mensajeria Externa Entregada, Código '
			+ codigo, CORREO, correo_remi)

		text_content = 'Sistema de Mensajeria'
		msg = EmailMultiAlternatives(
			subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		mensaje = 'La mensajeria ha sido cerrada.'
	except BadHeaderError:
		mensaje = 'No se pudo enviar el correo.'

	return mensaje
