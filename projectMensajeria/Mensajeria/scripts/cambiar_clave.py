from projectMensajeria.settings import PASS_LDAP
from django.contrib.auth.models import User
import os
from datetime import datetime

def run():
	usuario = User.objects.all().order_by('first_name')
	archivo = ''
	error = ''
	try:
		num=1
		archivo = open('log/usuario.txt', 'w')
		archivo.writelines('NOMBRE\t\t\t\t\t\t\t\t\tCORREO\t\t\t\t\t\t\t\t\t\tUSUARIO\n\n')
		
		for usuario in usuario:
			usuario.set_password(PASS_LDAP)
			usuario.save()

			archivo.writelines('%s - %s%s%s\n'
				% (num, usuario.get_full_name().ljust(40, " "), usuario.email.ljust(50, " "), usuario))
			num+=1

	except Exception as e:
		error = open('log/error_usuario.txt', 'w+')
		print('+-- No se pudo cambiar la clave --+')
		fecha = datetime.now()
		print(fecha)
		err = '%s ==> %s' %(fecha, e)
		error.writelines(err)
		error.close()
	finally:
		archivo.close()
