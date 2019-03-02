from django.contrib.auth.models import User, Group
from mitglieder.models import VereinsMitglied, offenePosten, Land, Beruf, Mitgliedsart, Kosten, Vortragsort, Adresse, Institution
from mitglieder.models import offenePosten, AboHeft, Abonnent
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, generics, permissions
from datetime import datetime as dt
from .serializers import UserSerializer, GroupSerializer, VereinsMitgliedSerializer, CountrySerializer, BerufeSerializer, MitgliedsartSerializer
from .serializers import KostenSerializer, VortragsortSerializer, AdresseSerializer, InstitutionenSerializer
from .serializers import AboHeftSerializer, AbonnentSerializer, offenePostenSerializer, CreateUserSerializer, LoginUserSerializer
from django.utils.encoding import force_text
from rest_framework.metadata import SimpleMetadata
from rest_framework.relations import ManyRelatedField, RelatedField
from django.views import View
from django.db.models import Q
from knox.models import AuthToken
from django.http import HttpResponse, FileResponse
import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from invoice.rechnung import createInvoice
from django.core.files.base import ContentFile
from PyPDF2 import PdfFileMerger
from django.core.mail import EmailMultiAlternatives



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


def sendmail(i):
    html_content = """
    <html><head></head><body>
    <h2>Hallo %s %s</h2>
    <h2>Danke, schön dass Sie am Geodätentag 2018 teilnehmen werden.</h2><br>
    <br>
    <p>Im Anhang der E-Mail befindet sich die pdf Rechnung.</p>
    <br>Bis bald in Steyr!<br><br>
    Ihr Geodätentag-Team<br>
    #wirsehenmehr
    </body></html>
    """ % (i.first_name, i.last_name)
    text_content = 'Danke, schön dass Sie am Geodätentag 2018 teilnehmen werden.'

    email = EmailMultiAlternatives('OVG Mitgliedsbeitrag', text_content, 'noreply@ovg.at', [i.email] )
    email.attach_alternative(html_content, "text/html")
    email.attach_file(i.rechnung.path)
    s = email.send()
    return s


def make_invoice(vm):
    dues = [(x.description, x.offen) for x in vm.offeneposten_set.filter(bezahlt=False)]

    invoice_date = datetime.datetime.now()

    m = { 'member_id': vm.mitgliedsnummer, 'invoice_date_str': invoice_date,
            'invoice_reference': '{}-{}'.format(vm.mitgliedsnummer, invoice_date.year),
            'invoice_recipient': "{first_name} {last_name}".format(**vm.__dict__),
            'invoice_to': '', 'invoice_street': vm.rechnungsadresse.strasse,
            'invoice_zip': vm.rechnungsadresse.plz, 'invoice_city': vm.rechnungsadresse.ort,
            'show_country': False, 'ovg_news': 'keine news', 'ovg_dues': dues
            }

    x = createInvoice(**m)
    invoice_filename = "ovg_inv_{}_{}.pdf".format(vm.id, invoice_date.strftime("%Y") )

    vm.rechnung.save(invoice_filename, ContentFile(x))
    
    return x


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
 
    for path in input_paths:
        pdf_merger.append(path)
 
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
 


class InvoiceView(View):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        vm = VereinsMitglied.objects.get(id=kwargs['id'])
        x = make_invoice(vm)
    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

        response.write(x)
        s = sendmail(vm)

        return response

    def post(self, request, *args, **kwargs):
        pass



def erlagscheine_anlegen(request):
    merged_filename = 'merged_pdf.pdf'
    v = VereinsMitglied.aktive.exclude(mitgliedsart__mitart="EM")
    vms = [vm for vm in v if vm.offeneposten_set.filter(bezahlt=False)] 
    # vms = vms[0:10]
    if vms:
        for vm in vms:
            make_invoice(vm)

        pfade = [vm.rechnung.path for vm in vms]
        merger(merged_filename, pfade)

        f = open(merged_filename, 'r')
        pdf = f.read()
        f.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={}'.format(merged_filename)
        response.write(pdf)
        return response 

    return HttpResponse("alle Beitraege sind einbezahlt")





class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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


class VereinsMitgliedViewSet(viewsets.ModelViewSet):
    queryset = VereinsMitglied.objects.all()
    serializer_class = VereinsMitgliedSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        if 'aktiv' in self.request.GET:
            vm = VereinsMitglied.aktive.all()
        else:
            vm = VereinsMitglied.objects.all()

        if 'wer' in self.request.GET:
            sn = self.request.GET['wer']
            vm = vm.filter(Q(last_name__icontains=sn) | Q(first_name__icontains=sn))
        if 'key' in self.request.GET and 'value' in self.request.GET:
            kwargs = {'{}'.format(self.request.GET['key']): self.request.GET['value'] }
            return vm.filter(**kwargs)
        return vm


class InstitutionenViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionenSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        if 'aktiv' in self.request.GET:
            inst = Institution.aktive.all()
        else:
            inst = Institution.objects.all()
        if 'wer' in self.request.GET:
            sn = self.request.GET['wer']
            inst = inst.filter(Q(institution_name__icontains=sn))
        if 'key' in self.request.GET and 'value' in self.request.GET:
            kwargs = {'{}'.format(self.request.GET['key']): self.request.GET['value'] }
            inst = inst.filter(**kwargs)
        return inst



class AboHeftViewSet(viewsets.ModelViewSet):
    queryset = AboHeft.objects.all()
    serializer_class = AboHeftSerializer
    metadata_class = MyMetaData


class offenePostenViewSet(viewsets.ModelViewSet):
    queryset = offenePosten.objects.all()
    serializer_class = offenePostenSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        ops = offenePosten.objects.all()
        if 'offen' in self.request.GET:
            if self.request.GET['offen'].lower() == "true":
                ops = ops.filter(bezahlt=False)
        return ops


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



def jahresbeitrag_anlegen(request):
    d = request.GET['jahr']
    context = {}
    if d!="":
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

        context['success'] = 'Der Beitrag "{}" wurde {} x erfolgreich angelegt!'.format(d, vms.count())
    else:
        context['error'] = 'Sie haben ein leeres Feld übergeben!'
    return JsonResponse(context)


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



def makepdfs(vorlage, target, m):
    template=get_template('mitglieder/'+vorlage)
    context={'vm': m}
    rendered_tmpl=template.render(context).encode('utf-8')
    path='/home/bipo/ovgreact/backend/mitgliederverwaltung/latexfiles'
    os.chdir(path)
    fname=target+'.tex'
    f=open(fname,'wb')
    f.write(rendered_tmpl)
    f.close()
    subprocess.call(['pdflatex',fname])
    pdffile=glob.glob(os.path.join(path,target+'.pdf'))
    shutil.copy(pdffile[0], os.path.join(settings.STATIC_ROOT,'pdfs'))
    files=glob.glob(os.path.join(path,target+'.*'))
    for f in files:
        os.remove(f)


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