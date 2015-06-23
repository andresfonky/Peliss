from django.contrib import admin
from . import models

class ShowFilm(admin.ModelAdmin):
    list_display = ('title', 'director', 'year')
    list_filter = ('year',)
    date_hierarchy = 'year'
    ordering = ('year',)

class ShowSeenFilms(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('films',)

class ShowWantedFilms(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('films',)

admin.site.register(models.Film, ShowFilm)
admin.site.register(models.SeenFilm, ShowSeenFilms)
admin.site.register(models.WantedFilm, ShowWantedFilms)