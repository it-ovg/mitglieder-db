from mitglieder.models import VereinsMitglied, offenePosten, Adresse
from mitglieder.models import offenePosten, AboHeft, Abonnent
from django.http import JsonResponse
import uuid

from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.metadata import SimpleMetadata
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.permissions import AllowAny

from datetime import datetime as dt
from api.serializers import VereinsMitgliedSerializer
from api.serializers import AboHeftSerializer, AbonnentSerializer, offenePostenSerializer
from django.utils.encoding import force_text
from django.views import View
from django.db.models import Q
from knox.models import AuthToken
from django.http import HttpResponse, FileResponse
import datetime
from reportlab.pdfgen import canvas
from invoice.rechnung import createInvoice
from invoice.abo import create_abo_invoice
from invoice.anniversary import create_anniversary
from django.core.files.base import ContentFile
from PyPDF2 import PdfFileMerger
from django.core.mail import EmailMultiAlternatives
import os
import shutil
from .views import merger, sendmail
from api.views.views import MyMetaData, make_abo_invoice, make_invoice



class VereinsMitgliedViewSet(viewsets.ModelViewSet):
    queryset = VereinsMitglied.objects.all()
    serializer_class = VereinsMitgliedSerializer
    metadata_class = MyMetaData


    def get_queryset(self):
        if 'aktiv' in self.request.GET:
            vm = VereinsMitglied.aktive.all()
        else:
            vm = VereinsMitglied.objects.all()

        if 'key' in self.request.GET and 'value' in self.request.GET:
            kwargs = {'{}'.format(self.request.GET['key']): self.request.GET['value'] }
            vm = vm.filter(**kwargs)

        namefilter = self.request.query_params.get('namefilter')
        if namefilter:
            vm = vm.filter(Q(last_name__icontains=namefilter) | Q(first_name__icontains=namefilter))
        return vm


    @action(detail=True, methods=['post'])
    def create_invoice(self, request, pk=None):
        news = ""
        if 'zahlscheinText' in request.data:
            news = request.data['zahlscheinText'].replace("<br>", "<br />")
        vm =self.get_object()
        x = make_invoice(vm, news=news)
        return HttpResponse(x)

    @action(detail=True, methods=['post'])
    def send_mail(self, request, pk=None):
        zahlscheinText = ""
        if 'zahlscheinText' in request.data:
            zahlscheinText = request.data['zahlscheinText'].replace("<br>", "<br />")
        emailText = ""
        if 'emailText' in request.data:
            emailText = request.data['emailText']

        print("emailText: {}".format(emailText))
        print("zahlscheinText: {}".format(zahlscheinText))
        vm =self.get_object()
        x = make_invoice(vm, news=zahlscheinText)
        s = sendmail(vm, content=emailText)
        return HttpResponse("das war ok")

    @action(detail=False, methods=['get'])
    def jahresbeitrag_anlegen(self, request):
        d = request.query_params.get('jahr')
        if d:
            year = int(d)
            stud_gebjahr = year-30
            vms = VereinsMitglied.aktive.exclude(mitgliedsart__mitart="EM")

            juniors = vms.filter(gebdat__year__gt=stud_gebjahr)
            for m in juniors:
                o = offenePosten(mitglied=m, description="Beitrag {}".format(d), offen=30, bezahlt=False, erstellt=dt.now())
                o.save()

            seniors = vms.filter(gebdat__year__lt=1945)
            for m in seniors:
                o = offenePosten(mitglied=m, description="Beitrag {}".format(d), offen=30, bezahlt=False, erstellt=dt.now())
                o.save()

            normale = vms.exclude(id__in=[s.id for s in seniors]).exclude(id__in=[j.id for j in juniors])
            for m in normale:
                o = offenePosten(mitglied=m, description="Beitrag {}".format(d), offen=55, bezahlt=False, erstellt=dt.now())
                o.save()

            message = 'Der Beitrag "{}" wurde {} x erfolgreich angelegt!'.format(d, vms.count())
            return Response(data=message, status=status.HTTP_200_OK)
        return Response(data="Sie haben ein leeres Feld übergeben.", status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['get'])
    def erlagscheine_anlegen(self, request):
        merged_filename = 'merged_pdf.pdf'
        v = VereinsMitglied.aktive.exclude(mitgliedsart__mitart="EM")
        vms = [vm for vm in v if vm.offeneposten_set.filter(bezahlt=False)] 
        vms = vms[0:5]
        if vms:
            for vm in vms:
                make_invoice(vm)

            pfade = [vm.rechnung.path for vm in vms]
            merger(merged_filename, pfade)

            f = open(merged_filename, 'r')
            pdf = f.read()
            f.close()
            return Response(data=pdf, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def jubilare_pdf(self, request):
        d = request.query_params.get('jahr')
        if d:
            year=int(d)
            jubls=[50,60,70,75,80,85,90,95]
            merged_filename = 'jubilare.pdf'
            folder = str(uuid.uuid4())
            path = '/tmp/{}'.format(folder)
            os.mkdir(path)
            os.chdir(path)
    
            vms=VereinsMitglied.aktive.order_by('gebdat').filter(gebdat__isnull=False)
            for m in vms:
                m.alter=year-m.gebdat.year
                if m.alter in jubls or m.alter>99:
                    mm = {'letter_date': m.gebdat.isoformat(), 'customer_salutation': 'Lieber', 
                        'customer_name': '{} {}'.format(m.first_name, m.last_name),
                        'customer_id': m.mitgliedsnummer, 'customer_anniversary': m.alter,
                        'letter_street': m.wohnadresse.strasse, 'letter_zip': m.wohnadresse.plz,
                        'letter_city': m.wohnadresse.ort, 'letter_country': m.wohnadresse.country.land,
                         }
                   
                    x = create_anniversary(**mm)
                    fname = str(uuid.uuid4())
                    f = open(fname, 'wb')
                    f.write(x)
                    f.close()

            pfade = os.listdir(path)
            merger(merged_filename, pfade)

            f = open(merged_filename, 'r')
            pdf = f.read()
            f.close()
            shutil.rmtree(path)
            return Response(data=pdf, status=status.HTTP_200_OK)
        return Response(data="Sie haben kein gültiges Jahr übergeben.", status=status.HTTP_406_NOT_ACCEPTABLE)

    """
    Args:
        letter_date: Datum des Briefes (= Geburtsdatum),
        letter_street: Strasse + Nr, 
        letter_zip: Postleitzahl, 
        letter_city: Stadt,
        letter_country: Land,
        customer_salutation: Anrede,
        customer_name: Name inkl. Titel,
        customer_id: Mitgliedsnummer,
        customer_anniversary: nter Geburtstag,
        generate_pdf: Soll ein PDF erzeugt werden, ansonst Buffer
    """

