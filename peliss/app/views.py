"""
Definition of views.
"""
from django.shortcuts import render, redirect, render_to_response
from django.http import Http404, HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.db.models import Q

from datetime import datetime, timedelta, date
import operator
from functools import reduce

from app.models import User, Film, SeenFilm, News, WantedFilm
from app.forms import UserProfileForm, EditProfileForm
from peliss.settings import EMAIL_HOST_USER

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def home(request):
    """Renders the home page."""
    current_user = request.user
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARNING")
    logger.error("ERROR")

    if request.user.is_authenticated():
        if request.user.finalizado is False:
            return redirect('/terminarPerfil')
        else:
            mylist = list()
            current_user = User.objects.get(username=current_user)
            amigos = current_user.amigos
            amigos = amigos.all()
            for amigo in amigos:
                if amigo.privado:
                    friend = User.objects.get(username=amigo.username)
                    friend = friend.amigos
                    friend = friend.all()
                    if current_user in friend:
                        mylist.append( Q(user = amigo) )
                else:
                    mylist.append( Q(user = amigo) )

            try:
                noticias = News.objects.filter(reduce(operator.or_, mylist)).order_by('-fecha').all
            except:
                noticias = None

            return render(
                request,
                'app/index.html',
                context_instance = RequestContext(request,
                {
                    'title':'Home Page',
                    'year':datetime.now().year,
                    'news':noticias,
                    'search':search,
                })
            )

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/peliss.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

#############################################################################################################
#USUARIO
def terminarPerfil(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            usuario = User.objects.get(username=current_user)
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.picture = request.FILES.get('picture')
            usuario.finalizado = True
            usuario.save()
            return redirect('/finPerfil')
    else:
        form = UserProfileForm

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['year'] = datetime.now().year,
    return render(request, 'app/terminarPerfil.html', args)

def finPerfil(request):
    current_user = request.user
    return render(
        request,
        'app/finPerfil.html',
        context_instance = RequestContext(request,
        {
            'user':current_user,
            'year':datetime.now().year,
        })
    )

def miPerfil(request):
    """Renders the contact page."""
    current_user = request.user
    logger.debug('miPderfil')
    if not request.user.picture:
        image = "/static/app/userphoto/default.png"
    else:
        image = request.user.picture.url

    current_user = current_user.username
    current_user = User.objects.get(username=current_user)
    amigos = current_user.amigos.all

    return render(
        request,
        'app/miPerfil.html',
        context_instance = RequestContext(request,
        {
            'user':current_user,
            'image':image,
            'amigos':amigos,
            'year':datetime.now().year,
        })
    )

def editarUsuario(request):
    current_user = request.user
    if request.method == 'POST':
         form = EditProfileForm(request.POST)
         if form.is_valid():
            usuario = User.objects.get(username=current_user)
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            if request.FILES.get('picture') is not None:
                usuario.picture = request.FILES.get('picture')
            usuario.privado = False
            if form.cleaned_data.get('privado') == True:
                usuario.privado = form.cleaned_data.get('privado')
            usuario.save()
            return redirect('/miPerfil')
         else:
            usuario = User.objects.get(username=current_user)
            logger.error(usuario)
            if form.cleaned_data.get('first_name') is not None:
                usuario.first_name = form.cleaned_data.get('first_name')
            if form.cleaned_data.get('last_name') is not None:
                usuario.last_name = form.cleaned_data.get('last_name')
            if request.FILES.get('picture') is not None:
                usuario.picture = request.FILES.get('picture')
            usuario.privado = False
            if form.cleaned_data.get('privado') == True:
                usuario.privado = form.cleaned_data.get('privado')            
            usuario.save()
            return redirect('/miPerfil')
    else:
        form = EditProfileForm

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['year'] = datetime.now().year,
    return render(request, 'app/editarUsuario.html', args)
 
def cambiarPrivado(request):
    current_user = request.user
    usuario = User.objects.get(username=current_user)
    if usuario.privado:
        usuario.privado = False
    else:
        usuario.privado = True

    usuario.save()

    html = "<html><body>User %s and privado %s.</body></html>" % (usuario.id, usuario.privado)
    return HttpResponse(html)

def misPelis(request):
    """Renders the contact page."""
    current_user = request.user
    some = True

    try:
        seen = SeenFilm.objects.get(user=current_user)
        visto = seen.films.all()
        return render(
        request,
            'app/misPelis.html',
            context_instance = RequestContext(request,
            {
                'films':visto,
                'some':some,
                'title':current_user,
                'year':datetime.now().year,
            })
        )
    except:
        some = False
        return render(
            request,
            'app/misPelis.html',
            context_instance = RequestContext(request,
            {
                'some':some,
                'title':current_user,
                'year':datetime.now().year,
            })
        )

def quieroVerPelis(request):
    """Renders the contact page."""
    current_user = request.user
    some = True

    try:
        seen = WantedFilm.objects.get(user=current_user)
        visto = seen.films.all()
        return render(
        request,
            'app/pelisQuieroVer.html',
            context_instance = RequestContext(request,
            {
                'films':visto,
                'some':some,
                'title':current_user,
                'year':datetime.now().year,
            })
        )
    except:
        some = False
        return render(
            request,
            'app/pelisQuieroVer.html',
            context_instance = RequestContext(request,
            {
                'some':some,
                'title':current_user,
                'year':datetime.now().year,
            })
        )

def recomendaciones(request):
    """Renders the contact page."""
    current_user = request.user
    some = True

    try: 
        num = SeenFilm.objects.get(user=current_user.id)
        num = str(num.id)
        seen = Film.objects.raw('SELECT F.GENRES, COUNT(*), TITLE FROM APP_SEENFILM_FILMS SF, APP_FILM F WHERE SF.FILM_ID = F.TITLE AND SEENFILM_ID =' + num + ' GROUP BY F.GENRES ORDER BY COUNT(F.GENRES) DESC LIMIT 1')
        for se in seen:
            generos = se.genres
            generos = generos.split(',')

        mylist = list()

        for genre in generos:
            genre = genre.replace(" ", "")
            mylist.append( Q(genres = genre) )

        films = Film.objects.filter(reduce(operator.or_, mylist)).all()

        return render(
        request,
            'app/recomendaciones.html',
            context_instance = RequestContext(request,
            {
                'films':films,
                'some':some,
                'year':datetime.now().year,
            })
        )

    except:
        some = False
        return render(
            request,
            'app/recomendaciones.html',
            context_instance = RequestContext(request,
            {
                'some':some,
                'year':datetime.now().year,
            })
        )

#########################################################################################################
#AMIGOS
def usuario(request, usuario):
    perfil = str(usuario)
    current_user = request.user  
    current_user = User.objects.get(username=current_user)

    noPrivate = True
    friends = False
    wanted = None
    fullWanted = False
    seen = None
    fullSeen = False

    perfil = User.objects.get(username=perfil)
    if perfil.privado:
        noPrivate = False

    if not perfil.picture:
        image = "/static/app/userphoto/default.png"
    else:
        image = perfil.picture.url

    if request.user.is_authenticated():
        try:
            amigos = User.objects.get(username=current_user, amigos=perfil)
            try:
                seen = SeenFilm.objects.get(user=perfil)
                seen = seen.films.all()
                fullSeen = True
            except:
                fullSeen = False

            try:
                wanted = WantedFilm.objects.get(user=perfil)
                wanted = wanted.films.all()
                fullWanted = True
            except:
                fullWanted = False

            friends = True
            try:
                amigos = User.objects.get(username=perfil, amigos=current_user)
                noPrivate = True
            except:
                friends = True
        except:
            friends = False

    return render(
        request,
        'app/usuario.html',
         context_instance = RequestContext(request,
        {
             'usuario': perfil,
             'amigos': friends,
             'noPrivate': noPrivate,
             'image': image,
             'wanted': wanted,
             'fullWanted': fullWanted,
             'seen': seen,
             'fullSeen': fullSeen,
             'year': datetime.now().year,
        })
    )

def addFriend(request, usuario):
    current_user = request.user
    current_user = current_user.username

    usuario = str(usuario)
    usuario = User.objects.get(username=usuario)

    current_user = User.objects.get(username=current_user)
    current_user.amigos.add(usuario)

    current_user.save()

    noticia = News(user=current_user.username, tipo=1, fecha = datetime.now(), descripcion= current_user.username + " ha anadido como amigo a " + usuario.username)
    noticia.save(force_insert=True)

    html = "<html><body>User %s and friend %s.</body></html>" % (current_user.id, usuario.id)
    return HttpResponse(html)

def deleteFriend(request, usuario):
    current_user = request.user
    current_user = current_user.username

    usuario = str(usuario)
    usuario = User.objects.get(username=usuario)

    current_user = User.objects.get(username=current_user)
    current_user.amigos.remove(usuario)

    current_user.save()

    noticia = News.objects.get(descripcion= current_user.username + " ha anadido como amigo a " + usuario.username).delete()

    html = "<html><body>User %s and friend %s.</body></html>" % (current_user.id, usuario.id)
    return HttpResponse(html)
###################################################################################################
#PELICULAS
def peliculas(request):
    """Renders the about page."""

    films = Film.objects.all().order_by('-counter')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/grid.html',
         context_instance = RequestContext(request,
        {
             'films': films,
             'title':'Peliculas',
             'year':datetime.now().year,
        })
    )

def film(request, pelicula):
    pelicula = str(pelicula)
    pelicula = pelicula.replace("%20", " ")
    pelicula = pelicula.replace("_", " ")
    
    current_user = request.user
    f = Film.objects.get(title=pelicula)
    error = False
    quiero = False

    if request.user.is_authenticated():
        try:
            seen = SeenFilm.objects.get(user=current_user, films=f)
            error = True
        except:
            error = False

        try:
            seen = WantedFilm.objects.get(user=current_user, films=f)
            quiero = True
        except:
            quiero = False

    return render(
        request,
        'app/film.html',
         context_instance = RequestContext(request,
        {
             'film':f,
             'seen':error,
             'wanted':quiero,
             'title':pelicula,
             'year':datetime.now().year,
        })
    )

def add(request, film):
    current_user = request.user

    film = str(film)
    film = film.replace("_", " ")

    f = Film.objects.get(title=film)

    try:
        visto = WantedFilm.objects.get(user=current_user)
        visto.films.remove(f)
        visto.save
    except:
        quiere = True

    try:
        seen = SeenFilm.objects.get(user=current_user)
        seen.films.add(f)
    except:
        seen = SeenFilm(user=current_user)
        seen.save()
        seen = SeenFilm.objects.get(user=current_user)
        seen.films.add(f)
        
    noticia = News(user=current_user.username, tipo=2, fecha = datetime.now(), descripcion= current_user.username + " ha visto la pelicula " + film)
    noticia.save(force_insert=True)
    f.counter += 1
    f.save()
    seen.save()

    html = "<html><body>Film %s and user %s.</body></html>" % (f.title, current_user.id)
    return HttpResponse(html)


def deleteAdd(request, film):
    current_user = request.user

    film = str(film)
    film = film.replace("_", " ")

    f = Film.objects.get(title=film)

    visto = SeenFilm.objects.get(user=current_user)
    visto.films.remove(f)
    visto.save
    
    noticia = News.objects.get(descripcion= current_user.username + " ha visto la pelicula " + film).delete()
    try:
        noticia = News.objects.get(descripcion= current_user.username + " quiere ver " + film).delete()
    except:
        None

    f.counter -= 1
    f.save()

    html = "<html><body>Film %s and user %s deleted seen.</body></html>" % (f.title, current_user.id)
    return HttpResponse(html)

def want(request, film):
    current_user = request.user

    film = str(film)
    film = film.replace("_", " ")

    f = Film.objects.get(title=film)

    try:
        seen = WantedFilm.objects.get(user=current_user)
        seen.films.add(f)
    except:
        seen = WantedFilm(user=current_user)
        seen.save()
        seen = WantedFilm.objects.get(user=current_user)
        seen.films.add(f)
        
    noticia = News(user=current_user.username, tipo=3, descripcion= current_user.username + " quiere ver " + film, fecha = datetime.now())
    noticia.save(force_insert=True)
    f.save()
    seen.save()

    html = "<html><body>Film %s and user %s want.</body></html>" % (f.title, current_user.id)
    return HttpResponse(html)

def deleteWant(request, film):
    current_user = request.user

    film = str(film)
    film = film.replace("_", " ")

    f = Film.objects.get(title=film)

    visto = WantedFilm.objects.get(user=current_user)
    visto.films.remove(f)
    visto.save
    
    noticia = News.objects.get(descripcion= current_user.username + " quiere ver " + film).delete()

    html = "<html><body>Film %s and user %s deleted want.</body></html>" % (f.title, current_user.id)
    return HttpResponse(html)


#SEARCH
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            films = Film.objects.filter(title__icontains=q).order_by('title')
            users = User.objects.filter(username__icontains=q).order_by('username')
            return render(request, 'app/search_results.html',
                {'films': films, 
                 'usuarios':users,
                 'query': q, 
                 'title':'Search', 
                 'year':datetime.now().year})

 
    return render(request, 'app/search_results.html', {'error':True, 'title':'Search', 'year':datetime.now().year})

#APLICACION
def contact(request):
    title = 'Contacto'
    return render(request, 'app/contact.html', {'title':title})

def tecnologias(request):
    current_user = request.user
    html = "<html><body>You are %s</body></html>" % (current_user)
    return HttpResponse(html)
#####################################################################
#EXAMPLES
def current_datetime(request):
    now = date.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def currentuser(request):
    current_user = request.user
    html = "<html><body>You are %s</body></html>" % current_user
    return HttpResponse(html)

def hours_ahead(request, plus):
    try:
        plus = int(plus)
    except ValueError:
        raise Http404()
    dt = datetime.now() + timedelta(hours=plus)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (plus, dt)
    return HttpResponse(html)

def web_browser(request):
    try:
        ua = request.META['HTTP_USER_AGENT']
    except KeyError:
        ua = 'unknown'
    ips = request.META['REMOTE_ADDR']
    html = "<html><body>Your browser is %s and your ip is %s</body></html>" % (ua, ips)
    return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

#EMAIL
def email(request):
    #send_mail(subject, message, from_email, to_list, fail_silently=True)
    send_mail('Email de prueba', 'Email de prueba', 'pelissdjango@gmail.com', ['fran10480@gmail.com', 'fonky_128gcc@hotmail.com'], fail_silently=True)
    html = "<html><body>Envio de email</body></html>"
    return HttpResponse(html)

def prueba(request):
    return render(request, 'app/prueba.html', {})