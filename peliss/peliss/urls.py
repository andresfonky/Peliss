"""
Definition of urls for peliss.
"""
from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^misPelis', 'app.views.misPelis', name='misPelis'),
    url(r'^peliculas$', 'app.views.peliculas', name='peliculas'),

    #login
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

    #Film 
    url(r'^film/([a-zA-Z0-9_]+)', 'app.views.film', name='film'),

    #Searh
    url(r'^search/$', 'app.views.search', name='search'),

    #Ejemplo current user
    url(r'^currentuser$', 'app.views.currentuser', name='currentuser'),

    #Ejemplo añadir bd
    url(r'^add/([a-zA-Z0-9_]+)', 'app.views.add', name='add'),
    
    #Ejemplo basico tiempo
    url(r'^time/$', 'app.views.current_datetime', name='current_datetime'),
    url(r'^time/plus/(\d{1,2})', 'app.views.hours_ahead', name='hours_ahead'),

    #Web Browser
    url(r'^browser/$', 'app.views.web_browser', name='web_browser'),
    url(r'^meta/$', 'app.views.display_meta', name='display_meta('),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # REGISTRATION
    #url(r'^rango/', include('rango.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)
