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
                o = offenePosten(institution=inst, description="Beitrag {}".format(year), offen=55, bezahlt=False, erstellt=datetime.datetime.now())
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
                news = 'Aufgrund von Umstellungsarbeiten der Mitgliedsdatenbank können wir den Mitgliedsbeitrag 2019 erst jetzt aussenden. Der Einfachheit halber schicken wir auch gleich jenen von 2020. Wir danken für Ihre Unterstützung und Ihre True zur OVG.'
                news = """
                wir haben im Jahr 2019 unsere Mitgliederverwaltung auf neue Beine gestellt. Dies hat dann doch mehr Zeit 
                in Anspruch genommen, als wir zu Beginn des Vorhabens dachten. Aus diesem Grund war es nicht möglich im 
                vergangenen Jahr Zahlscheine für den Mitgliedsbeitrag auszusenden.<br/>
 
                Nun sind wir aber so weit und können Ihnen die entsprechende Vorschreibung des Mitgliedsbeitrages übermitteln. 
                Da eine Doppelaussendung innerhalb weniger Wochen wohl keinen Sinn hat, haben wir uns dazu entschlossen, 
                die Mitgliedsbeiträge der Jahre 2019 (so Sie diesen nicht aus eigenem Antrieb überweisen haben) und 2020 
                auf einem Zahlschein gemeinsam vorzuschreiben. Wir danken für Ihre Geduld.<br/>

                Wir bitten um Einzahlung des ausständigen Betrages bis Ende April 2020. Sollten Sie Telebanking verwenden, 
                geben Sie bitte „MitgliedsNr/2020“ als Zahlungsreferenz ein.<br/><br/>

                PS.: Sollte bei der Migration Ihrer Daten ein Fehler passiert sein, bitten wir um eine Nachricht an 
                office@ovg.at um diesen korrigieren zu können – danke.<br/>

		PPS.: Bitte im Kalender eintragen: Geodätentag Steyr 13-16. April 2021. Wir freuen uns auf Ihr kommen!
                """

                make_invoice(inst, news)

            pfade = [inst.rechnung.path for inst in insts]
            merger(merged_filename, pfade)

            f = open(merged_filename, 'r')
            pdf = f.read()
            f.close()
            return Response(data=pdf, status=status.HTTP_200_OK)


