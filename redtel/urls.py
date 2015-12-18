#redtel URL Configuration

from django.conf.urls import patterns, url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login,logout

urlpatterns = patterns('',
						(r'^admin/', include(admin.site.urls) ),
                       url(r'^$', 'portal.views.index', name='index'),
                       url(r'^ingresar$', login, {'template_name': 'login.html', }, name="login"),
                       url(r'^home/$', 'portal.views.home', name='home'),
                       url(r'^us/$', 'portal.views.us', name='us'),
                       url(r'^home/mensajes/$', 'portal.views.mensajes', name='mensajes'),
                       url(r'^home/mensajes/eliminar/(?P<id>[0-9]+)/$', 'portal.views.eliminar'),
                       url(r'^home/mensajes/nuevo_mensaje$', 'portal.views.nuevo_mensaje', name='nuevo_mensaje'),
                       url(r'^home/mis_datos/$', 'portal.views.mis_datos', name='mis_datos'),
                       url(r'^home/mis_datos/obtener_certificado$', 'portal.views.obtener_certificado', name='obtener_certificado'),
                       url(r'^home/mis_liquidaciones/$', 'portal.views.mis_liquidaciones', name='mis_liquidaciones'),
                       url(r'^home/mis_liquidaciones/imprimir_liquidacion/(?P<pk>[0-9]+)/$', 'portal.views.imprimir_liquidacion', name='imprimir_liquidacion'),
                       url(r'^home/cargar_usuarios/$', 'portal.views.cargar_usuarios', name='cargar_usuarios'),
                       url(r'^home/cargar_liquidaciones/$', 'portal.views.cargar_liquidaciones', name='cargar_liquidaciones'),
                       url(r'^home/cargar_liquidaciones/carga_correcta$', 'portal.views.carga_correcta', name='carga_correcta'),
                       url(r'^logout$', logout, {'template_name': 'index.html', }, name="logout"),
)

