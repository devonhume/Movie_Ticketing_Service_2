from django.contrib import admin
from django.urls import path
from django.core import serializers
from ninja import NinjaAPI
# import movie_server.movie_ticketing.ticket_handler as th
# import movie_server.movie_ticketing.models as models
import datetime as dt
import json

# from movie_server.movie_ticketing.ticket_handler import TicketHandler

api = NinjaAPI()

# handler = TicketHandler()
#
#
# @api.get("/get-current-movies")
# def get_current_movies(request):
#     movies = models.Movie.objects.exclude(id__exact=0)
#     movie_list = serializers.serialize('json', movies)
#     return movie_list
