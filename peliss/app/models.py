"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
     user = models.ForeignKey(User)

     def __unicode__(self):
         return User.username

class Film(models.Model):
    title = models.CharField(primary_key=True, max_length=30)
    director = models.CharField(max_length=50)
    year = models.DateField()
    country = models.CharField(max_length=30)
    counter = models.IntegerField()
    image = models.CharField(max_length=30) 

    def __unicode__(self):
        return title

class SeenFilm(models.Model):
     user = models.ForeignKey(User)
     films = models.ManyToManyField(Film)

     def __unicode__(self):
        return user.username

