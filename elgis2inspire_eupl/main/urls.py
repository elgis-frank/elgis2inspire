#-------------------------------------------------------
# Datei main.urls.py Version 1.01 
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
    path('impressum', views.impressum, name='impressum'),
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('clscheme', views.clscheme, name='clscheme'),
    path('wfs', views.wfs, name='wfs'),
    path('linkurl/<str:link>', views.linkurl, name='linkurl'),
    path('capaedit/<int:zahl>', views.capaedit, name='capaedit'),
    path('capa/<int:zahl>', views.capa, name='capa'),
    path('test',views.test,name='test'),
    path('uebersicht', views.uebersicht, name='uebersicht'),
]
