from django import forms
from .models import HabitatList
from django.utils.html import format_html




class GeodatForm(forms.Form):    
    datei      = forms.FileField(label='Wählen Sie für die Geodaten eine geojson Datei') # Geodatensatz
    spfid = forms.CharField(label='Attributname der featureid')
    splcode = forms.CharField(label='Attributname des Biotoptyps')
    spn2000 = forms.CharField(label='Attributname des Lebensraumtyps')
    nmspace = forms.CharField(label='Namespace des Habitatdatensatzes (Basis URL)')

class attributForm(forms.Form):
    csvdat = forms.FileField(label='Wählen Sie die csv Datei') # csv Datensatz
    

class HabitatListForm(forms.ModelForm):
       

    class Meta:
        model = HabitatList
        
        match_choice = ( ('congruent','kongruent'), ('excludes', 'schließt aus'), ('includedIn', 'enthalten'), ('includes','enthält'), ('overlaps', 'überlappt'))
        fields = ['lcode', 'lname', 'icode', 'iname', 'imatch', 'hlid', 'localid']
        labels = {
            'lcode': ('Localcode'),
            'lname': ('Localname'),
            'icode': ('EUNIS Code'),
            'iname': ('EUNIS Name'),
            'imatch': ('Übereinstimmung'),
            'localid':('atom-id'),
            
            
        }
        widgets = {
            'localid': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'lcode': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'lname': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'icode': forms.HiddenInput(),
            "iname": forms.Textarea(attrs={"onclick": "startTree()", "cols": 40, "rows": 1}),
            'imatch': forms.Select(choices=match_choice),
            'hlid': forms.HiddenInput(),
            
            
        }
        



