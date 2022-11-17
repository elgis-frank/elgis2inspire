#!/usr/bin/python3
"""
WSGI config for elgis2inspire project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/

Programming by eLGIS
               
      Copyright (C) by elgis ( https://elgis.de ) 2022
 Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
 Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
 zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inspire.settings')

application = get_wsgi_application()
