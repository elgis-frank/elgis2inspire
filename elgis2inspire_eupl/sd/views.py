#-------------------------------------------------------
# Datei sd.views.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import HttpResponse,QueryDict, HttpResponseRedirect
from .models import SpeciesDistributionUnit, DistributionInfoType, SpeciesDistributionDataSet, DocumentCitation, CitationUrl, faultguid
from main.models import Capabilities
from django.views.generic.edit import UpdateView
from django.template import loader
from .forms import  sdFormdataset
from .functions.functions import  dels, handle_uploaded_sdfile, dellocalid, delfaultguid, addCapabilities
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import json

@login_required
def sd(request):
    return render(request, 'sd.html', {})

@login_required
def sdgeo(request):
    from .models import SpeciesDistributionDataSet
    from .forms import sdGeoForm
    data_select = request.POST.get('data_select', 'Null')
    nmsp = request.POST.get('nmsp', 'Null')
    name = request.POST.get('name', 'Null')
    fid = request.POST.get('fid', 'Null')
    
    if request.method == 'POST':
        sdgeo = sdGeoForm(request.POST, request.FILES)  
        if sdgeo.is_valid():
            ergebnis = handle_uploaded_sdfile(request.FILES['datei'], data_select, nmsp, name, fid, )
            messages.info(request, ergebnis)
            return render(request, 'sdgeook.html')  
    else:
        initial = {'nmsp':'https://elgis.de','fid':'featureid','name':'name',}
        sdgeo = sdGeoForm(initial=initial)  
        return render(request,"sdgeo.html",{'form':sdgeo})

@login_required
def delsd(request):
    from .models import SpeciesDistributionUnit
    from .forms import delGeoForm
    if request.method == 'POST':
        sddi = request.POST.get('data_select', 'Null')
        ergebnis = dels(sddi)
        messages.info(request, ergebnis)
        return render(request, 'sdokdel.html')
    else:
        delgeo = delGeoForm()
        return render(request,"delgeounit.html",{'form':delgeo})
    
def delnomen(request):
    ergebnis = delfaultguid()
    messages.info(request, ergebnis)
    return render(request, 'sdok.html')


@login_required
def sdStart(request):
    sdfirst = SpeciesDistributionDataSet.objects.filter().first()
    sdform =   sdFormdataset(instance=sdfirst)
    sddi = sdfirst.sddi
    sdlast = SpeciesDistributionDataSet.objects.filter().last()
    erste = sdfirst.sddi
    letzte = sdlast.sddi
    next = sddi + 1
    return render(request,"sdd.html",{'sddi':sddi,'form':sdform,'erste':erste,'letzte':letzte,'actual':sddi,'next':next,}) 


@login_required
def sdEdit(request, sddi, sig):
    sdfirst = SpeciesDistributionDataSet.objects.filter().first()
    sdform =   sdFormdataset(instance=sdfirst)
    sdlast = SpeciesDistributionDataSet.objects.filter().last()
    erste = sdfirst.sddi
    letzte = sdlast.sddi
    next = sddi + 1
    prev = sddi -1
    if sig == 'go':
        inst = SpeciesDistributionDataSet.objects.get(pk=sddi)
        sdform = sdFormdataset(instance=inst)
        return render(request,"sdd.html",{'sddi':letzte,'form':sdform,'erste':erste,'letzte':letzte,'actual':sddi,'next':next,'prev':prev})
    elif sig == 'neu':
        letzte = letzte + 1
        sddi = letzte
        initial = {'namespace':'https://elgis.de', 'versionId':'1.0', 'keywords_eng':'wms,wfs,species distribution'}
        sdform = sdFormdataset(initial=initial)
        return render(request,"sdneu.html",{'form':sdform,'sddi':1})



@login_required
def sdin(request):
    if request.method == 'POST':
        sddi = request.POST.get("localID")
        if not sddi:
            try:
                f = sdFormdataset(request.POST)
                if f.is_valid():
                    f.save()
            except (KeyError):
                render(request, 'listein.html', {} )
            sd = SpeciesDistributionDataSet.objects.filter().last()
            id = sd.pk
            sd.localID = id
            sd.save(update_fields=["localID"])
            ergebnis = addCapabilities(id)
            messages.info(request, ergebnis)
            cap = Capabilities.objects.get(sddi=id)
            cid = cap.cid
            #zunächst die pk ermitteln
            lista = []
            capall = Capabilities.objects.all()
            leng = len(capall)
            lista = list(capall)
            cidnr = []
            for i in lista:
                cidnr.append(i.pk)
            for c in range(leng):
                if cidnr[c] == cid:
                    zahl = c
            return render(request, 'sdok.html',{'zahl':zahl}) 
        else:
            try:
                s = SpeciesDistributionDataSet(pk=sddi)
                f = sdFormdataset(request.POST, instance=s)
                f.save()
            except (KeyError):
                render(request, 'listein.html', {} )
            ergebnis1 = 'der Datensatz Nr. ' +sddi+' wurde geändert'
            messages.info(request, ergebnis1)
            return render(request, 'sdoke.html',{})         
    else:
        #initial = {'namespace':'http://naturschutz.rlp.de', 'versionId':'1.0', 'keywords_eng':'wms,wfs,species distribution'}
        #fo = sdFormdataset(initial=initial)       
        return  redirect('/sdStart')
    


@login_required
def deldat(request):
    from .models import SpeciesDistributionDataSet
    from .forms import delGeoForm
    if request.method == 'POST':
        sddi = request.POST.get('data_select', 'Null')
        ergebnis = dellocalid(sddi)
        messages.info(request, ergebnis)
        return render(request, 'sdokdel.html')
    else:
        delgeo = delGeoForm()
        return render(request,"delgeo.html",{'form':delgeo})
        
@login_required
def nonNomen(request):
    nnomen = faultguid.objects.values_list('name').order_by('name')
    return render(request, 'nnomen.html', {'arten':nnomen})
