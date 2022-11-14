#-------------------------------------------------------
# Datei main.views.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

from dataclasses import replace
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ps.models import ProtectedSite
from sd.models import SpeciesDistributionUnit, SpeciesDistributionDataSet
from hb.models import HabitatTypeCoverType, HabitatList
from main.forms import CapabilitiesForm
from main.models import Capabilities
from .functions.functions import getbbox, writeDok
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def index(request):
    return render(request, 'index2.html', {})

def impressum(request):
    return render(request, 'impressum.html', {})

@login_required
def start(request):
    return render(request, 'start1.html', {})

def wfs(request):
   
    d ={}
    surl = {}
    snam = {}
    snamex = {}
    surlex = {}
    surlwms = {}
    surlwmsex = {}
    urlget = {}
    urlgetex = {}
    anzahlps = ProtectedSite.objects.filter().count()
    if anzahlps > 0:
        d["gs"] = "/cgi-bin/wfs/ps_wfs?service=wfs&version=2.0.0&request=GetFeature&typenames=ProtectedSite&count=10"
        d["cs"] = "/cgi-bin/wfs/ps_wfs?service=wfs&version=2.0.0&request=GetCapabilities"
        d["ss"] = "/cgi-bin/wfs/ps_wfs?service=wfs&version=2.0.0&request=DescribeFeatureType&typenames=ProtectedSite"
        d["wmspg"] = "/cgi-bin/wfs/ps_wms?service=wms&version=1.1.1&request=GetMap&Layers=PS.ProtectedSite"
        d["wmspc"] = "/cgi-bin/wfs/ps_wms?service=wms&version=1.3.0&request=GetCapabilities"
        box = getbbox('ps_protectedsite')
        b0 = str(box[0][0])
        b1 = str(box[0][1])
        b2 = str(box[0][2])
        b3 = str (box[0][3])
        d["wmspg"] = "/cgi-bin/wfs/ps_wms?service=wms&version=1.3.0&request=GetMap&layers=PS.ProtectedSite&bbox="+ b1 + "," + b0 + "," + b3 + "," + b2 + "&width=200&height=100&crs=EPSG:3035&format=image/png&Styles=default"
        d["wmspc"] = "/cgi-bin/wfs/ps_wms?service=wms&version=1.3.0&request=GetCapabilities&"
    anzahlhb = HabitatTypeCoverType.objects.filter().count()
    if anzahlhb > 0:
        d["gb"] = "/cgi-bin/wfs/hb_wfs?service=wfs&version=2.0.0&request=GetFeature&typenames=Habitat&count=10"
        d["cb"] = "/cgi-bin/wfs/hb_wfs?service=wfs&version=2.0.0&request=GetCapabilities"
        d["sb"] = "/cgi-bin/wfs/hb_wfs?service=wfs&version=2.0.0&request=DescribeFeatureType&typenames=Habitat"
        box = getbbox('hb_habitat')
        b0 = str(box[0][0])
        b1 = str(box[0][1])
        b2 = str(box[0][2])
        b3 = str (box[0][3])
        d["wmshg"] = "/cgi-bin/wfs/hb_wms?service=wms&version=1.3.0&request=GetMap&layers=hb.Habitat&bbox="+ b1 + "," + b0 + "," + b3 + "," + b2 + "&width=200&height=100&crs=EPSG:3035&format=image/png&Styles=default"
        d["wmshc"] = "/cgi-bin/wfs/hb_wms?service=wms&version=1.3.0&request=GetCapabilities&"
    
    sp = SpeciesDistributionDataSet.objects.values('localID', 'name')
    #anzahlsdlsd = SpeciesDistributionUnit.objects.filter().count()
    #if anzahlsd > 0:
    for i in sp:
        zahl1 = i['localID']
        zahl = str(zahl1)
        name = i['name']
        url = "/cgi-bin/wfs/sd_d" + zahl + "_wfs?service=wfs&version=2.0.0&"
        box = getbbox('sd_speciesdistributionunit')
        b0 = str(box[0][0])
        b1 = str(box[0][1])
        b2 = str(box[0][2])
        b3 = str (box[0][3])
        urlwms = "/cgi-bin/wfs/sd_d" + zahl + "_wms?service=wms&version=1.3.0&request=GetMap&layers=SD._ReferenceSpeciesCodeValue_&bbox="+ b0 + "," + b1 + "," + b2 + "," + b3 + "&width=200&height=100&srs=EPSG:3035&format=image/png&Styles=default"
        #hier wird ein getmap example hergestellt
        fexemp = SpeciesDistributionUnit.objects.filter(sddi=zahl).first()
        if not fexemp:
            exempm = 'Milvus milvus'
        else:
            exempm = fexemp.referenceSpeciesName
        exemp = exempm.replace(' ','') #Leerzeichen im Namen entfernen
        urlg = "/cgi-bin/wfs/sd_d" + zahl + "_wms?service=wms&version=1.3.0&request=GetMap&layers=SD."+exemp+"&bbox="+ b1 + "," + b0 + "," + b3 + "," + b2 + "&width=200&height=100&crs=EPSG:3035&format=image/png&Styles=default"
        #urlthomas = "/cgi-bin/wfs/sd_d1_wms?service=wms&version=1.1.1&request=GetMap&layers=SD.Milvusmilvus&bbox="+ b0 + "," + b1 + "," + b2 + "," + b3 + "&width=200&height=100&srs=EPSG:3035&format=image/png"
        surl[zahl] = url
        surlwms[zahl] = urlwms
        urlget[zahl] = urlg
        snam[zahl] = name
    for f in surl.keys():
        gesamt = SpeciesDistributionUnit.objects.filter(sddi=f).count()
        if gesamt > 0:
            #nur wenn daten vorhanden werden urls angelegt            
            snamex[f] = snam[f]
            surlex [f] = surl[f]
            surlwmsex[f] = surlwms[f]
            urlgetex[f] = urlget[f]
    return render(request, 'wfs.html', {'d':d, 'surlex':surlex, 'snamex':snamex, 'surlwmsex':surlwmsex, 'urlthomas':urlgetex})

def clscheme(request):
    listl = list(HabitatList.objects.filter().values())
    return render(request, 'showlist1.html', {'list': listl})

def linkurl(request,link):
    wahldic = {'biowfs':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/hb_wfs?service=wfs&version=2.0.0&request=GetCapabilities', 'biowms':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/hb_wms?service=wms&version=1.3.0&request=GetCapabilities&',
    'pswfs':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/ps_wfs?service=wfs&version=2.0.0&request=GetCapabilities','pswms':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/ps_wms?service=wms&version=1.3.0&request=GetCapabilities&',
    'sdwfs':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/sd_d1_wfs?service=wfs&version=2.0.0&service=wfs&version=2.0.0&request=GetCapabilities','sdwms':'https://inspire.naturschutz.rlp.de/cgi-bin/wfs/sd_d1_wms?service=wms&version=1.3.0&request=getCapabilities&'}
    url = wahldic[link]
    return render(request, 'copy.html', {'link':url})


@login_required
def capa(request, zahl):
    lista = []
    capall = Capabilities.objects.all()
    leng = len(capall)
    lista = list(capall)
    cidnr = []
    for i in lista:
        cidnr.append(i.pk)
    letzte = leng-1
    cid = cidnr[zahl]
    letzte = leng-1
    erste = 0
    next = zahl + 1
    actual = zahl
    prev = zahl - 1
    inst = Capabilities.objects.get(cid=cid)
    cform = CapabilitiesForm(instance=inst)
    layer = inst.inspirelayer
    sddi = inst.sddi
    return render(request,"capa.html",{'form':cform,'erste':erste,'letzte':letzte,'actual':actual,'next':next,'prev':prev,'layer':layer,'sddi':sddi}) 

@login_required
def capaedit(request, zahl):
    #zunächst die zahl vom pk ermitteln, da pk nicht durchgängig ist, sondern 2 3 4 15 17 etc muss eine Liste dazwischengeschaltet werden
    lista = []
    capall = Capabilities.objects.all()
    leng = len(capall)
    lista = list(capall)
    cidnr = []
    for i in lista:
        cidnr.append(i.pk)
    cid = cidnr[zahl] #pk
    if request.method == 'POST':
        inst = Capabilities(pk=cid)
        inh = Capabilities.objects.get(cid=cid)
        layer = inh.inspirelayer
        sddi = inh.sddi
        f = CapabilitiesForm(request.POST,instance=inst)
        try:
            if f.is_valid():
                f.save()
                antwort = writeDok(layer,sddi)
        except (KeyError):
            render(request, 'listein.html', {} )
    #return HttpResponseRedirect(reverse('capa', kwargs={'cid':cid}))
        messages.info(request, antwort)
        return render(request,"capok.html", {'zahl':zahl})
    else:
        return HttpResponseRedirect(reverse('capa', kwargs={'zahl':zahl}))

@login_required
def test(request):
    return render(request,"tests.html",{})

def uebersicht(request):
    arten = SpeciesDistributionUnit.objects.values_list('referenceSpeciesName').order_by('referenceSpeciesName').distinct()
    return render(request, 'uebersicht1.html', {'arten':arten})

