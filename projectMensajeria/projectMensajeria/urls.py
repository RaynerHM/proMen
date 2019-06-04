"""projectMensajeria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Mensajeria import views

urlpatterns = [
	path('prueba/', views.prueba, name='prueba'),
	
	path('cambiar_estado_ajax/', views.cambiar_estado_ajax,
		name='cambiar_estado_ajax'),
	
	path('admin/', admin.site.urls),
	
	path('login/', views.login, name='login'),
	
	path('logout/', views.logout, name='logout'),
	
	path('reporte/', views.reporte, name='reporte'),
	
	path('', views.mensajeria_personal, name='publico'),
	
	path('entregar_mensajeria_ajax/', views.entregar_mensajeria_ajax,
		name='entregar_mensajeria_ajax'),
	
	path('cargar_departamentos_ajax/', views.cargar_departamentos_ajax,
		name='cargar_departamentos_ajax'),
	
	path('cargar_usuarios_ajax/', views.cargar_usuarios_ajax,
		name='cargar_usuarios_ajax'),
	
	path('registrar_mensajeria_interna/', views.registrar_mensajeria_interna,
		name='registrar_mensajeria_interna'),
	
	path('registrar_mensajeria_externa/', views.registrar_mensajeria_externa,
		name='registrar_mensajeria_externa'),
	
	path('detalles_mensajeria_externa_ajax/', 
		views.detalles_mensajeria_externa_ajax,
		name='detalles_mensajeria_externa_ajax'),
	
	path('detalles_mensajeria_interna_ajax/',
		views.detalles_mensajeria_interna_ajax,
		name='detalles_mensajeria_interna_ajax'),
		
]
admin.site.site_header = 'Admin - Control de Mensajeria'
