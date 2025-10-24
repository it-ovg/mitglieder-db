from mitglieder.models import offenePosten, Land, Beruf, Mitgliedsart, Kosten, Vortragsort, Adresse, Institution
from .views import MyMetaData
from api.serializers import InstitutionenSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from invoice.rechnung import createInvoice
import datetime
from django.core.files.base import ContentFile
from api.views.views import merger
from rest_framework.response import Response


def make_invoice(inst, news=''):
    dues = [(x.description, x.offen) for x in inst.offeneposten_set.filter(bezahlt=False)]

    invoice_date = datetime.datetime.now()

    m = { 'member_id': inst.mitgliedsnummer, 'invoice_date_str': invoice_date,
            'invoice_reference': '{}-{}'.format(inst.mitgliedsnummer, invoice_date.year),
            'invoice_recipient': "{institution_name}".format(**inst.__dict__),
            'invoice_to': '', 'invoice_street': inst.rechnungsadresse.strasse,
            'invoice_zip': inst.rechnungsadresse.plz, 'invoice_city': inst.rechnungsadresse.ort,
            'show_country': True, 'ovg_news': news, 'ovg_dues': dues,
            'invoice_deadline': datetime.date(2020,2,29)
            }

    x = createInvoice(**m)
    invoice_filename = "ovg_inv_inst_{}_{}.pdf".format(inst.id, invoice_date.strftime("%Y") )

    inst.rechnung.save(invoice_filename, ContentFile(x))
    
    return x



class InstitutionenViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionenSerializer
    metadata_class = MyMetaData

    def get_queryset(self):
        if 'aktiv' in self.request.GET:
            inst = Institution.aktive.all()
        else:
            inst = Institution.objects.all()
        
        if 'key' in self.request.GET and 'value' in self.request.GET:
            kwargs = {'{}'.format(self.request.GET['key']): self.request.GET['value'] }
            inst = inst.filter(**kwargs)

        namefilter = self.request.query_params.get('namefilter')
        if namefilter:
            inst = inst.filter(institution_name__icontains=namefilter)
        return inst


    @action(detail=False, methods=['get'])
    def jahresbeitrag_anlegen(self, request):
        d = request.query_params.get('jahr')
        if d:
            year = int(d)
            ii = Institution.aktive.exclude(mitgliedsart__mitart__in=["AD"]).filter(kostenart__art__in=["M"])

            for inst in ii:
                o = offenePosten()
                o = offenePosten(institution=inst, description="Beitrag {}".format(year), offen=65, bezahlt=False, erstellt=datetime.datetime.now())
                o.save()

            message = 'Der Beitrag "{}" wurde {} x erfolgreich angelegt!'.format(d, ii.count())
            return Response(data=message, status=status.HTTP_200_OK)
        return Response(data="Sie haben ein leeres Feld übergeben.", status=status.HTTP_406_NOT_ACCEPTABLE)


    @action(detail=False, methods=['get'])
    def erlagscheine_anlegen(self, request):
        merged_filename = '/tmp/merged_inst_pdf.pdf'
        ii = Institution.aktive.all()
        ii = Institution.aktive.exclude(mitgliedsart__mitart__in=["AD", "DA"]).filter(kostenart__art__in=["M"])

        insts = [i for i in ii if i.offeneposten_set.filter(bezahlt=False)] 
        # vms = vms[0:5]
        if insts:
            for inst in insts:
                news = """
                Liebe OVG Mitglieder,<br /><br />

                mit diesem Erlagschein dürfen wir Ihnen den Mitgliedsbeitrag für das Jahr 2024 vorschreiben und uns recht herzlich für ihre jährliche Unterstützung der OVG bedanken. Diese Aussendung bietet darüber hinaus die Gelegenheit ihre bei uns hinterlegte Emailadresse zu kontrollieren, über die sie registriert sind und viele interessante Infos zur OVG erhalten. <br />
                Ihre Emailadresse lautet: {}<br />
                Sollte diese Emailadresse nicht korrekt sein, ersuchen wir sie uns das per Email unter office@ovg.at mitzuteilen. <br /><br />
            
                Beste Grüße<br />
                Ihre OVG<br /><br />

                PS: Sollten sich Ihre Adressdaten ändern, einfach Email an office@ovg.at.<br />
                PPS: Wir ersuchen um Einzahlung des ausständigen Betrages bis Ende Oktober 2024. Bei Telebanking bitte als Zahlungsreferenz „{}/2024“ an    geben.<br />
                """.format(inst.email, inst.mitgliedsnummer)
                make_invoice(inst, news)

            pfade = [inst.rechnung.path for inst in insts]
            merger(merged_filename, pfade)

            f = open(merged_filename, 'r')
            pdf = f.read()
            f.close()
            return Response(data=pdf, status=status.HTTP_200_OK)


