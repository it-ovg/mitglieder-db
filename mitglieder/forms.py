from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LandForm(ModelForm):
    class Meta:
        model=Land
        exclude=['']

class KostenForm(ModelForm):
    class Meta:
        model=Kosten
        exclude=['']

class offenePostenForm(ModelForm):
    class Meta:
        model=offenePosten
        exclude=['mitglied','erstellt','bezahltam']

class MitgliedsartForm(ModelForm):
    class Meta:
        model=Mitgliedsart
        exclude=['']

class BerufForm(ModelForm):
    class Meta:
        model=Beruf
        exclude=['']

class VereinsMitgliedForm(ModelForm):
    class Meta:
        model=VereinsMitglied
        exclude=['password','last_login','is_superuser','groups','user_permissions']
