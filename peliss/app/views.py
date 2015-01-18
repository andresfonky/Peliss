"""
Definition of views.
"""
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpRequest
from django.template import RequestContext
from app.models import Film, SeenFilm

from datetime import datetime
from datetime import timedelta

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

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

def currentuser(request):
    current_user = request.user
    html = "<html><body>You are %s</body></html>" % (current_user)
    return HttpResponse(html)

def film(request, pelicula):
    pelicula = str(pelicula)
    pelicula = pelicula.replace("_", " ")

    current_user = request.user
    f = Film.objects.get(title=pelicula)
    error = False

    try:
        seen = SeenFilm.objects.get(user=current_user)
        visto = seen.films.all()
        for peli in visto:
            if(peli.title == pelicula):
                error = True
    except:
        error = False

    return render(
        request,
        'app/film.html',
         context_instance = RequestContext(request,
        {
             'film':f,
             'seen':error,
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
        seen = SeenFilm.objects.get(user=current_user)
        seen.films.add(f)
    except:
        seen = SeenFilm(user=current_user)
        seen.save()
        seen = SeenFilm.objects.get(user=current_user)
        seen.films.add(f)
        
    f.counter += 1
    f.save()
    seen.save()

    html = "<html><body>Film %s and user %s.</body></html>" % (f.title, current_user.id)
    return HttpResponse(html)

#Search
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            films = Film.objects.filter(title__icontains=q)
            return render(request, 'app/search_results.html',
                {'films': films, 'query': q, 'title':'Search', 'year':datetime.now().year})
 
    return render(request, 'app/search_results.html', {'error':True, 'title':'Search', 'year':datetime.now().year})

#####################################################################
def current_datetime(request):
    now = datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
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

