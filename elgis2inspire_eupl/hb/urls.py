#-------------------------------------------------------
# Datei hb.urls.py Version 1.01 
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
    path('hb', views.hb, name='hb'),
    path('delhb', views.delhb, name='delhb'),
    path('eingabe', views.eingabe, name='eingabe'),
    path('edit/<int:rang>', views.edit, name='fedit'),
    path('editfind', views.editfind, name='editfind'),
    path('update/<int:rang>', views.update, name='update'),
    path('insert', views.insert, name='insert'),
    path('insertsave', views.insertsave, name='insertsave'),
    path('geodat', views.geodat, name='geodat'),
    path('getCode', views.getCode, name='getCode'),
    path('getName', views.getName, name='getName'),
    path('cl/<str:code>', views.cl, name='cl'),
    path('csvlist', views.csvlist, name='csvlist'),
    path('dellist/<str:rang>', views.dellist, name='dellist'),
    path('attributdat', views.attributdat, name='attributdat'),
 ]
