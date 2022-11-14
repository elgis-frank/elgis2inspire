#-------------------------------------------------------
# Datei hb.views.py Version 1.01 
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
from django.http import HttpResponse, HttpResponseRedirect
from .models import  HabitatList
from sd.models import SpeciesDistributionUnit
from .forms import attributForm, GeodatForm, HabitatListForm
from .functions.functions import handle_uploaded_file, handle_uploaded_attfile, dele, fillRang, gethlid
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required , permission_required
import json, csv
from django.template.defaulttags import register


@login_required
def hb(request):
    return render(request, 'hb.html', {})

@login_required
def delhb(request):
    ergebnis = dele()
    messages.info(request, ergebnis)
    return render(request, 'delok.html') 

@login_required
def eingabe(request):
    return render(request, 'listein.html', {})


@login_required
@permission_required('hb.edit_list') 
def edit(request, rang):
    gesamt = HabitatList.objects.all()
    if gesamt.exists(): 
        hblistF = HabitatList.objects.filter().first()
        erste = hblistF.rang
        hblistL = HabitatList.objects.filter().last()
        letzte = hblistL.rang
        lid = rang
        next = int(lid)+1
        prev = int(lid)-1
        if prev < erste:
            prev = erste
        if lid > letzte:
           lid = letzte
        hblist = HabitatList.objects.get(rang=rang)
        #neue codelist id übernehmen
        localid = hblist.localid
        f = HabitatListForm(instance=hblist)
        #f = HabitatListForm()
        if rang > 528:
            delete = "True"
        else:
            delete = "False"
        update = "True"
        plus = "True"
        return  render(request, 'edit.html', {'delete':delete,'plus':plus,'localid':localid,'actual':rang,'erste':erste, 'letzte':letzte,'next':next, 'prev':prev, 'update':update,'form': f})
    else:
        meldung = 'Sie müssen erst eine Biotopschlüsselliste laden!'
        messages.info(request, meldung)
        return render(request, 'geook.html') 
       

@login_required
@permission_required('hb.edit_list')
def editfind(request):
    data = request.POST
    code = data["code"]
    name = data["name"]
   
    if code:
        hblist = HabitatList.objects.get(lcode=code)
    else:
        hblist = HabitatList.objects.get(lname=name)
    #id bestimmen
    alid = hblist.rang
    #erste und letzte bestimmen
    f = HabitatListForm(instance=hblist)
    hblistF = HabitatList.objects.filter().first()
    erste = hblistF.rang
    hblistL = HabitatList.objects.filter().last()
    letzte = hblistL.rang
    #weitere Parameter
    nlid = int(alid)+1
    prev = int(alid)-2
    if prev < erste:
        prev = erste
    if nlid > letzte:
        nlid = letzte
    if alid > 530:
        delete = "True"
    else:
        delete = "False"
    update = "False"
    plus = "True"
    return  render(request, 'edit.html', {'delete':delete,'plus':plus,'actual':alid,'erste':erste, 'letzte':letzte,'next':nlid, 'prev':prev, 'update':update,'form': f})
    #return render(request, 'edit.html',{'b':bl,'form': f,})
    


@login_required
@permission_required('hb.edit_list')
def update(request, rang):
    #data = request.POST
    #b = data["bl"]
    #inst = HabitatList.objects.get(hlid=hlid)
    hlid = gethlid(rang)
    try:
        inst = HabitatList(pk=hlid)
        f = HabitatListForm(request.POST,instance=inst)
        HabitatList.objects.filter(rang=rang).delete()
        #f = HabitatListForm(request.POST)
        if f.is_valid():
            f.save()
        fillRang()
    except (KeyError):
        render(request, 'listein.html', {} )
           
    return HttpResponseRedirect(reverse('fedit', kwargs={'rang':rang}))
    #return render(request, 'testup.html' , {'form':f})


@login_required
@permission_required('hb.edit_list')
def insert(request):
    hblistL = HabitatList.objects.filter().last()
    letzte = hblistL.rang
    f = HabitatListForm()
    plus = "False"
    update = "False"
    return  render(request, 'edit.html', { 'letzte':letzte,'plus':plus, 'update':update,'form': f})

@login_required
@permission_required('hb.edit_list')
def insertsave(request ):
    try:
        f = HabitatListForm(request.POST)
        if f.is_valid():
            f.save()
    except (KeyError):
        render(request, 'listein.html', {} )
    fillRang()
    hblistL = HabitatList.objects.last()
    letzte = hblistL.rang
    return HttpResponseRedirect(reverse('fedit', kwargs={'rang':letzte}))

@login_required
@permission_required('hb.edit_list')
def dellist(request, rang):
    rang1 = int(rang)
    if rang1 > 528: #Grunddatensatz
        HabitatList.objects.filter(rang=rang1).delete()
        fillRang()
        rang1 = 528
        return HttpResponseRedirect(reverse('fedit', kwargs={'rang':rang1}))
    else:
        message = 'Einträge der Basisliste können nicht gelöscht werden'
        return  render(request, 'listok.html',{'messages':message})




@login_required
def geodat(request):
    spfid = request.POST.get('spfid', 'Null')
    splcode = request.POST.get('splcode', 'Null')
    spn2000 = request.POST.get('spn2000', 'Null')
    nmspace = request.POST.get('nmspace', 'Null')
    
    if request.method == 'POST':
        #if Habitat.objects.filter(bl=buland).exists():
         #   anzahl = Habitat.objects.filter(bl=buland).count()
          #  return render(request, "pruefgeodat.html",{ "bltext":buland,"anzahl":anzahl})
        geodat = GeodatForm(request.POST, request.FILES)  
        if geodat.is_valid():
            ergebnis = handle_uploaded_file(request.FILES['datei'], spfid, splcode, spn2000, nmspace)
            messages.info(request, ergebnis)
            return render(request, 'geook.html')  
    else:
        initial = {'spfid':'featureid','splcode':'lcode','spn2000':'n2000','nmspace':'https://elgis.de'}  
        geodat = GeodatForm(initial=initial)  
        return render(request,"geodat.html",{'form':geodat}) 

@login_required
def attributdat(request):
    if request.method == 'POST':  
        if HabitatList.objects.filter().exists():
            anzahl = HabitatList.objects.filter().count()
            return render(request, "prueflist.html",{ "anzahl":anzahl})
            #return HttpResponse("Hier sind noch Daten")
        attdat = attributForm(request.POST, request.FILES) 
        if attdat.is_valid():
            response = handle_uploaded_attfile(request.FILES['csvdat'])
            messages.info(request, response)
            return render(request, 'listok.html')  
    else:  
        attdat = attributForm()  
        return render(request,"attdat.html",{'form':attdat}) 


@login_required
#ajax Abfrage
def getCode(request):
    code = request.GET.get('search', 'NULL')
    cdata = HabitatList.objects.filter(lcode__startswith=code)
    codelist = list(cdata.values('lcode'))
    codelist2 = []
    for i in codelist:
        codelist2.append(i['lcode'])
    jcode = json.dumps(codelist2)
    response = HttpResponse(jcode,content_type='application/json')
    return response

@login_required
#ajax Abfrage
def getName(request):
    name = request.GET.get('search', 'NULL')
    ndata = HabitatList.objects.filter(lname__startswith=name)
    namelist = list(ndata.values('lname'))
    namelist2 = []
    for i in namelist:
        namelist2.append(i['lname'])
    jname = json.dumps(namelist2)
    response = HttpResponse(jname,content_type='application/json')
    return response

def cl(request, code):
    hblist = HabitatList.objects.filter().get(lcode=code)
    return render(request, 'getlist.html', {'list': hblist,})


def csvlist(request):
    # Create the HttpResponse object with the appropriate CSV header.
    #response = HttpResponse(content_type='text/csv', headers={'Content-Disposition':'attachment', 'filename':"habitatlist.csv",})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="habitatlist.csv"'
    listl = list(HabitatList.objects.filter().values())
    writer = csv.writer(response)
    writer.writerow(['localid', 'lcode', 'lname', 'icode', 'iname', 'imatch'])
    for i in range(len(listl)):
        writer.writerow([listl[i]['localid'],listl[i]['lcode'],listl[i]['lname'], listl[i]['icode'], listl[i]['iname'], listl[i]['imatch']])
    return response

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@login_required
def attributdat(request):
    if request.method == 'POST':  
        #if HabitatList.objects.filter(bl=buland).exists():
            #anzahl = HabitatList.objects.filter(bl=buland).count()
            #return render(request, "prueflist.html",{ "bltext":buland,"anzahl":anzahl})
            #return HttpResponse("Hier sind noch Daten")
        attdat = attributForm(request.POST, request.FILES) 
        if attdat.is_valid():
            response = handle_uploaded_attfile(request.FILES['csvdat'])
            messages.info(request, response)
            return render(request, 'error.html')  
    else:  
        attdat = attributForm()  
        return render(request,"attdat.html",{'form':attdat}) 



