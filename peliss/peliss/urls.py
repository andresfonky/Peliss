"""
Definition of urls for peliss.
"""
from datetime import datetime
from django.conf import settings
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Examples:
    url(r'^$', 'app.views.home', name='home'),
    #REGISTRATION
    url(r'^accounts/', include('registration.backends.default.urls')),
    #USUARIO
    url(r'^terminarPerfil', 'app.views.terminarPerfil', name='terminarPerfil'),
    url(r'^finPerfil', 'app.views.finPerfil', name='finPerfil'),
    url(r'^miPerfil$', 'app.views.miPerfil', name='miPerfil'),
    url(r'^editarUsuario', 'app.views.editarUsuario', name='editarUsuario'),
    url(r'^misPelis', 'app.views.misPelis', name='misPelis'),
    url(r'^amigos', 'app.views.amigos', name='amigos'),
    #PELICULAS
    url(r'^peliculas$', 'app.views.peliculas', name='peliculas'),
    url(r'^film/([a-zA-Z0-9_]+)', 'app.views.film', name='film'),
    # ADMIN
    url(r'^admin/', include(admin.site.urls)),
    #APLICACION
    url(r'^tecnologias', 'app.views.tecnologias', name='tecnologias'),
    url(r'^contact', 'app.views.contact', name='contact'),

    #LOGIN
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    #SEARCH
    url(r'^search/$', 'app.views.search', name='search'),

    #IMAGENES
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    #OTROS
    #Ejemplo current user
    url(r'^currentuser$', 'app.views.currentuser', name='currentuser'),
    #Ejemplo add bd
    url(r'^add/([a-zA-Z0-9_]+)', 'app.views.add', name='add'),
    #Ejemplo basico tiempo
    url(r'^time/$', 'app.views.current_datetime', name='current_datetime'),
    url(r'^time/plus/(\d{1,2})', 'app.views.hours_ahead', name='hours_ahead'),
    #Web Browser
    url(r'^browser/$', 'app.views.web_browser', name='web_browser'),
    url(r'^meta/$', 'app.views.display_meta', name='display_meta('),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #email
    url(r'^email', 'app.views.email', name='email'),
)
