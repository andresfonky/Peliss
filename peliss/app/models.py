"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
User.add_to_class('picture', models.ImageField(null=True,blank=True, upload_to='userphoto'))
User.add_to_class('amigos', models.ManyToManyField('self', symmetrical=False, blank=True))
User.add_to_class('finalizado', models.BooleanField(default=False))
User.add_to_class('privado', models.BooleanField(default=False))

class Film(models.Model):
    title = models.CharField(primary_key=True, max_length=80)
    director = models.CharField(max_length=50)
    year = models.DateField()
    country = models.CharField(max_length=90)
    genres = models.CharField(max_length=90, default= 'None')
    raiting = models.IntegerField(default = 0)
    counter = models.IntegerField()
    image = models.CharField(max_length=200) 

    def __unicode__(self):
        return title

class SeenFilm(models.Model):
     user = models.ForeignKey(User)
     films = models.ManyToManyField(Film)

     def __unicode__(self):
        return user.username

class WantedFilm(models.Model):
     user = models.ForeignKey(User)
     films = models.ManyToManyField(Film)

     def __unicode__(self):
        return user.username

class News(models.Model):
     user = models.CharField(max_length=30)
     tipo = models.IntegerField()
     fecha = models.DateTimeField(default=datetime.now)
     descripcion = models.CharField(max_length=255)

     def __unicode__(self):
        return user.username