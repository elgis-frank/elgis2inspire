#-------------------------------------------------------
# Datei sd.urls.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

from django.urls import path, include
from . import views


urlpatterns = [
    path('sd', views.sd, name='sd'),
    path('sdgeo', views.sdgeo, name='sdgeo'),
    path('delsd', views.delsd, name='delsd'),
    path('sdin', views.sdin, name='sdin'),
    path('deldat', views.deldat, name='deldat'),
    path('nonNomen', views.nonNomen, name='nonNomen'),
    path('delnomen', views.delnomen, name='delnomen'),
    path('sdEdit/<int:sddi>/<str:sig>', views.sdEdit, name='sdEdit'),
    path('sdStart', views.sdStart, name='sdStart'),
    path('sdin', views.sdin, name='sdin'),
    #path('sdneu', views.sdneu, name='sdneu'),
 ]
