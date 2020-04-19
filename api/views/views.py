from django.contrib.auth.models import User, Group
from mitglieder.models import VereinsMitglied, offenePosten, Land, Beruf, Mitgliedsart, Kosten, Vortragsort, Adresse, Institution
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
from api.serializers import UserSerializer, GroupSerializer, VereinsMitgliedSerializer, CountrySerializer, BerufeSerializer, MitgliedsartSerializer
from api.serializers import KostenSerializer, VortragsortSerializer, AdresseSerializer, InstitutionenSerializer
from api.serializers import AboHeftSerializer, AbonnentSerializer, offenePostenSerializer, CreateUserSerializer, LoginUserSerializer
from django.utils.encoding import force_text
from django.views import View
from django.db.models import Q
from knox.models import AuthToken
from django.http import HttpResponse, FileResponse
import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from invoice.rechnung import createInvoice
from invoice.abo import create_abo_invoice
from invoice.anniversary import create_anniversary
from invoice.envelope import create_envelope_bev, create_envelope_aut, create_envelope_int
from django.core.files.base import ContentFile
from PyPDF2 import PdfFileMerger
from django.core.mail import EmailMultiAlternatives
import os
import shutil


class MyMetaData(SimpleMetadata):
    def get_field_info(self, field):
        field_info = super(MyMetaData, self).get_field_info(field)
        if isinstance(field, (RelatedField, ManyRelatedField)):
            if hasattr(field, 'view_name'):
                if field.view_name != 'adresse-detail':
                    field_info['choices'] = [
                        {
                            'value': choice_value,
                            'display_name': force_text(choice_name, strings_only=True)
                        }
                        for choice_value, choice_name in field.get_choices().items()
                    ]
        return field_info


def sendmail(i, content=""):
    html_content = "<html><head></head><body><h2>Hallo {} {}</h2>{}</body></html>".format(i.first_name, i.last_name, content)
    text_content = 'Danke, schön dass Sie am Geodätentag 2018 teilnehmen werden.'

    email = EmailMultiAlternatives('OVG Mitgliedsbeitrag', text_content, 'noreply@ovg.at', [i.email] )
    email.attach_alternative(html_content, "text/html")
    email.attach_file(i.rechnung.path)
    s = email.send()
    return s


def make_invoice(vm, news=''):
    dues = [(x.description, x.offen) for x in vm.offeneposten_set.filter(bezahlt=False)]

    invoice_date = datetime.datetime.now()

    m = { 'member_id': vm.mitgliedsnummer, 'invoice_date_str': invoice_date,
            'invoice_reference': '{}-{}'.format(vm.mitgliedsnummer, invoice_date.year),
            'invoice_recipient': "{first_name} {last_name}".format(**vm.__dict__),
            'invoice_to': vm.namenszusatz, 'invoice_street': vm.rechnungsadresse.strasse,
            'invoice_zip': vm.rechnungsadresse.plz, 'invoice_city': vm.rechnungsadresse.ort,
            'invoice_country': vm.rechnungsadresse.country.land,
            'show_country': True, 'ovg_news': news, 'ovg_dues': dues,
            'invoice_deadline': datetime.date(2020,2,29)
        }

    x = createInvoice(**m)
    invoice_filename = "ovg_inv_{}_{}.pdf".format(vm.id, invoice_date.strftime("%Y") )

    vm.rechnung.save(invoice_filename, ContentFile(x))
    
    return x


def make_abo_invoice(vm):
    book_price = 50.0
    invoice_date = datetime.datetime.now()

    m = { 'customer_id': vm.kundennummer, 'customer_vat_id': vm.uid,
            'abo_id': vm.kundennummer,
            'abo_year': 2019,
            'debt_claim': 100, 'discount': vm.heftsum*book_price*vm.prozent,
            'book_amount': vm.heftsum,
            'book_price': book_price,
            'invoice_date_str': invoice_date,
            'inv_company': vm.name,
            'inv_department': vm.name2,
            'inv_name': vm.name3,
            'inv_street': vm.rechnungsanschrift.strasse,
            'inv_zip':vm.rechnungsanschrift.plz ,
            'inv_city': vm.rechnungsanschrift.ort,
            'inv_country': vm.rechnungsanschrift.country.land,
            }

    x = create_abo_invoice(**m)
    invoice_filename = "ovg_inv_abo_{}_{}.pdf".format(vm.id, invoice_date.strftime("%Y") )

    vm.rechnung.save(invoice_filename, ContentFile(x))
    
    return x


def make_etiketten(vms, abos, inst, wohin='BEV'):
    if wohin == 'BEV':
        make_pdf = create_envelope_bev
        merged_filename = 'etiketten_bev.pdf'
    elif wohin == 'AUT':
        make_pdf = create_envelope_aut
        merged_filename = 'etiketten_aut.pdf'
    elif wohin == 'INT':
        make_pdf = create_envelope_int
        merged_filename = 'etiketten_int.pdf'

    folder = str(uuid.uuid4())
    path = '/tmp/{}'.format(folder)
    os.mkdir(path)
    os.chdir(path)

    for vm in vms:
        if vm.lieferadresse and vm.heftanzahl:
            print(vm.id)
            land = 'Austria'
            if not vm.first_name:
                rname = vm.last_name
            else:
                rname = "{} {}".format(vm.first_name,vm.last_name)

            if vm.lieferadresse.country:
                land = vm.lieferadresse.country.land
            mm = {
                "recipient_id": vm.mitgliedsnummer,
                "recipient_name": rname,
                "recipient_extra": vm.namenszusatz,
                "recipient_street": vm.lieferadresse.strasse,
                "recipient_zip": vm.lieferadresse.plz,
                "recipient_city": vm.lieferadresse.ort,
                "recipient_postbox": vm.lieferadresse.pobox,
                "recipient_country": land,
            }

            x = make_pdf(**mm)
            for i in range(vm.heftanzahl):
                fname = str(uuid.uuid4())
                f = open(fname, 'wb')
                f.write(x)
                f.close()

    for im in inst:
        if im.lieferadresse and im.heftanzahl:
            print(im.id)
            land = 'Austria'
            if im.lieferadresse.country:
                land = im.lieferadresse.country.land
            mm = {
                "recipient_id": im.mitgliedsnummer,
                "recipient_name": im.institution_name,
                "recipient_extra": im.name2,
                "recipient_street": im.lieferadresse.strasse,
                "recipient_zip": im.lieferadresse.plz,
                "recipient_city": im.lieferadresse.ort,
                "recipient_postbox": im.lieferadresse.pobox,
                "recipient_country": land,
            }

            x = make_pdf(**mm)
            for i in range(im.heftanzahl):
                fname = str(uuid.uuid4())
                f = open(fname, 'wb')
                f.write(x)
                f.close()

    for ab in abos:
        land = 'Austria'
        if ab.country and ab.heftanzahl:
            land = ab.country.land
            if not ab.vorname:
                aname = ab.nachname
            else:
                "{} {}".format(ab.vorname, ab.nachname)
            mm = {
                "recipient_id": ab.kundennummer,
                "recipient_name": aname,
                "recipient_extra": ab.surname2,
                "recipient_street": ab.strasse,
                "recipient_zip": ab.plz,
                "recipient_city": ab.ort,
                "recipient_postbox": ab.pobox,
                "recipient_country": land,
            }

            x = make_pdf(**mm)
            for i in range(ab.heftanzahl):
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
    return pdf




def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
 
    for path in input_paths:
        pdf_merger.append(path)
 
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
 






class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginAPI(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Land.objects.all().order_by('land')
    serializer_class = CountrySerializer


class BerufeViewSet(viewsets.ModelViewSet):
    queryset = Beruf.objects.order_by('bezeichnung')
    serializer_class = BerufeSerializer


class MitgliedsartViewSet(viewsets.ModelViewSet):
    queryset = Mitgliedsart.objects.all()
    serializer_class = MitgliedsartSerializer


class KostenViewSet(viewsets.ModelViewSet):
    queryset = Kosten.objects.all()
    serializer_class = KostenSerializer


class VortragsortViewSet(viewsets.ModelViewSet):
    queryset = Vortragsort.objects.all()
    serializer_class = VortragsortSerializer


class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    metadata_class = MyMetaData



class AbonnentViewSet(viewsets.ModelViewSet):
    queryset = Abonnent.objects.all()
    serializer_class = AbonnentSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        if 'aktiv' in self.request. GET:
            abos = Abonnent.aktive.all()
        else:
            abos = Abonnent.objects.all()
        if 'wer' in self.request.GET:
            abos = abos.filter(Q(name__icontains=self.request.GET['wer']))
        return abos


    @action(detail=True, methods=['get'])
    def create_invoice(self, request, pk=None):
        vm =self.get_object()
        x = make_abo_invoice(vm)
        return HttpResponse(x)

    @action(detail=True, methods=['get'])
    def send_mail(self, request, pk=None):
        vm =self.get_object()
        x = make_abo_invoice(vm)
        s = sendmail(vm)
        return HttpResponse("das war ok")

    @action(detail=False, methods=['get'])
    def etiketten(self, request):
        if 'wohin' in self.request.GET:
            wohin = self.request.GET['wohin']
            if wohin in ['BEV', 'AUT', 'INT']:
                vms = VereinsMitglied.aktive.all().filter(heftanzahl__gt=0)
                abos = AboHeft.objects.filter(aboende__isnull=True)
                inst = Institution.aktive.all()

                if wohin == 'BEV':
                    vms = vms.filter(versand__iexact='BEV')
                    abos = []
                    inst = inst.filter(versand__iexact='BEV')
                else:
                    vms = vms.filter(versand__iexact='POST')
                    inst = inst.filter(versand__iexact='POST')
                    l = Land.objects.filter(land='AUSTRIA')

                    if wohin == 'AUT':
                        vms = vms.filter(lieferadresse__country__in=l)
                        abos = abos.filter(country__in=l)
                        inst = inst.filter(lieferadresse__country__in=l)
                    elif wohin == 'INT':
                        vms = vms.exclude(lieferadresse__country__in=l)
                        abos = abos.exclude(country__in=l)
                        inst = inst.exclude(lieferadresse__country__in=l)

                pdf = make_etiketten(vms, abos, inst, wohin)
                if abos:
                    print("\n\n\nEs waren insgesamt {} abos".format(abos.count()))
                return Response(data=pdf, status=status.HTTP_200_OK)

        return Response(data="Sie haben keinen gültigen <<WOHIN>> Wert übergeben.", status=status.HTTP_406_NOT_ACCEPTABLE)













class AboHeftViewSet(viewsets.ModelViewSet):
    queryset = AboHeft.objects.all()
    serializer_class = AboHeftSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        if 'aktiv' in self.request. GET:
            abos = AboHeft.objects.filter(aboende__isnull=True)
        else:
            abos = AboHeft.objects.all()
        if 'wer' in self.request.GET:
            abos = abos.filter(Q(name__icontains=self.request.GET['wer']))
        return abos


class offenePostenViewSet(viewsets.ModelViewSet):
    queryset = offenePosten.objects.all()
    serializer_class = offenePostenSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        ops = offenePosten.objects.all()
        if 'offen' in self.request.GET:
            ops = ops.filter(bezahlt=False)

        namefilter = self.request.query_params.get('namefilter')
        if namefilter:
            ops = ops.filter(Q(description__icontains=namefilter) | Q(mitglied__first_name__icontains=namefilter) | Q(mitglied__last_name__icontains=namefilter))
        return ops.filter(mitglied__isnull=False).filter(mitglied__in=VereinsMitglied.aktive.all())


    @action(detail=True, methods=['get'])
    def set_bezahlt(self, request, pk=None):
        op =self.get_object()
        op.bezahlt = True
        op.bezahlt_am = datetime.datetime.now()
        op.zahlung = op.offen
        op.save()
        serializer = offenePostenSerializer(op, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)





def dashboard(request):
    year=dt.now().year
    if 'jahr' in request.GET:
        year=int(request.GET['jahr'])
    mm=VereinsMitglied.aktive.order_by('gebdat').filter(gebdat__isnull=False)
    for m in mm:
        m.alter=year-m.gebdat.year
    jubls=[50,60,70,75,80,85,90,95]
    jubilare=[{'alter': m.alter, 'first_name': m.first_name, 'last_name': m.last_name, 'gebdat': m.gebdat, 'monat': m.gebdat.month} for m in mm if m.alter in jubls or m.alter>99]
    oo=offenePosten.objects.filter(bezahlt=False)
    summe=0
    for o in oo:
        if o.offen:
            summe=summe+o.offen
    context = { 'offenerbetrag': int(summe*100)/100, 'abonnentcount': Abonnent.objects.count(), 'aboheftcount': AboHeft.objects.count(),
                'mitgliedercount': {'aktiv': VereinsMitglied.aktive.count(), 'inaktiv': VereinsMitglied.objects.filter(storndat__isnull=False).count()}, 
                'institutionencount': {'aktiv': Institution.objects.filter(storndat__isnull=True).count(), 'inaktiv': Institution.objects.filter(storndat__isnull=False).count() },
                'jubilare': jubilare, 'kosten': Kosten.objects.count(), 'mitgliedsarten': Mitgliedsart.objects.count(), 'berufecount': Beruf.objects.count(), 'laendercount': Land.objects.count() }
    return JsonResponse(context)



def pdf(request, was):
    vms = VereinsMitglied.aktive.filter(heftanzahl>0)
    if was == "hauspost":
        bevler = vms.filter(versand='BEV')
        makepdfs('hauspost_vorlage.tex', 'hauspost', bevler)
    
    vms = vms.filter(versand='POST')
    if was == "austria":
        l = Land.objects.filter(land='AUSTRIA')
        austria = vms.filter(wohnadresse__country__in=l).order_by('plz')
        makepdfs('austria_vorlage.tex', 'austria', austria)

    if was == "europa":
        l=Land.objects.filter(EU=True).exclude(land='AUSTRIA')
        europa = vms.filter(wohnadresse__country__in=l)
        makepdfs('europa_vorlage.tex', 'europa', europa)

    if was == "international":
        l = Land.objects.filter(EU=False)
        international=vms.filter(wohnadresse__country__in=l)

    return render(request, 'mitglieder/vgiuebersicht.html', context)
