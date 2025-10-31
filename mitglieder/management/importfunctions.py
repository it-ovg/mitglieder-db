from ..models import Anrede, Beruf, Kosten, Land, Mitgliedsart, Versand, Titel, Institution
from ..models import offenePosten, Vortragold, VereinsMitglied, Vortragsort, Adresse, Abonnent, AboHeft
import pandas as pd
from datetime import datetime as dt
import codecs
from random import randint
from django.contrib.auth.models import User, Group
import uuid

def import_olddb():
    offenePosten.objects.all().delete()
    Institution.objects.all().delete()
    VereinsMitglied.objects.all().delete()
    Anrede.objects.all().delete()
    Adresse.objects.all().delete()
    Land.objects.all().delete()
    Beruf.objects.all().delete()
    Kosten.objects.all().delete()
    Mitgliedsart.objects.all().delete()
    Titel.objects.all().delete()
    Versand.objects.all().delete()
    Vortragold.objects.all().delete()
    Vortragsort.objects.all().delete()

    gruppen = ['Finanz', 'Manager', 'VGI', 'User', 'Admin']
    for g in gruppen:
        d, c = Group.objects.get_or_create(name=g)

    df = pd.read_csv('mitglieder/olddb/ANREDE.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        a=Anrede(oldid=r[0],anrede=r[1])
        a.save()
    a=Anrede(oldid=29)
    a.save()

    df = pd.read_csv('mitglieder/olddb/BERUF.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        b=Beruf(oldid=r[0],beruf=r[1],bezeichnung=r[2])
        b.save()

    Kosten(art="-",bezeichnung="Kein Eintrag").save()
    Kosten(art="T",bezeichnung="Tausch").save()
    Kosten(art="F",bezeichnung="Frei").save()
    Kosten(art="M",bezeichnung="Mitgliedsbeitrag").save()
    Kosten(art="K",bezeichnung="dasweisskeiner").save()
    Kosten(art="P",bezeichnung="what_the_fuck_is_____P____?").save()

    Versand(versand="P",bezeichnung="POST").save()
    Versand(versand="B",bezeichnung="BEV").save()
    Versand(versand="-",bezeichnung="kein Versand").save()


    df = pd.read_csv('mitglieder/olddb/LAND.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        l=Land(oldid=r[0],land=r[1],iso=r[2],EU=r[3])
        l.save()

    df = pd.read_csv('mitglieder/olddb/MITART.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        m=Mitgliedsart(mitart=r[0],bezeichnung=r[1],anmerkung=r[2])
        m.save()


    df = pd.read_csv('mitglieder/olddb/TITEL.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        t=Titel(oldid=r[0],titel=r[1])
        t.save()

    df = pd.read_csv('mitglieder/olddb/VORTRAG.txt',delimiter=';',encoding="latin-1")
    for i,r in df.iterrows():
        v=Vortragold(oldid=r[0],Vortragsort=r[1])
        v.save()



    VereinsMitglied.objects.all().delete()

    f = codecs.open('mitglieder/olddb/HISTORY.txt', 'r', 'latin-1')
    ll = f.readlines()[1:]
    f.close()

    for ind, line in enumerate(ll):
        l = line.replace("\r\n","").split(';')
        if l[22] != '': 
            gebdat=dt.strptime(l[22],'%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d')
        else:
            gebdat=None

        if l[15] != '': 
            beidat=dt.strptime(l[15],'%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d')
        else:
            beidat=None

        if l[16] != '':
            storndat=dt.strptime(l[16],'%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d')
        else:
            storndat=dt(1900,1,1)

        
        t = ''
        if l[2] != '':
            tf = Titel.objects.filter(oldid=int(l[2]))
            if tf: 
                t = tf.first().titel

        if l[20] == '':
             k=None
        else:
            k=Kosten.objects.get(art=l[20])

        if l[27] == '' or l[27] == '0': b=None
        else: b=Beruf.objects.get(oldid=int(l[27]))

        if l[1] == '' or l[1] == '0': anr=None
        else: anr=Anrede.objects.get(oldid=int(l[1])).anrede

        if l[21] == '': v=None
        else: v=Versand.objects.get(versand=l[21]).bezeichnung

        if l[19] == '': m=None
        else: m=Mitgliedsart.objects.get(mitart=l[19])

        heftanz = l[29]
        if heftanz == '': heftanz = 0

        mnr = l[0]
        if mnr == '': 
            mnr = 99999
            username = str(uuid.uuid1())[0:18]
        else:
            username = mnr
        
        lid = l[11]
        if l[11] == '': lid=1
        land, c = Land.objects.get_or_create(oldid=int(lid), defaults={'land': 'unknown', 'iso':'ISO'})   
        pobox = l[7]
        if pobox == '': pobox = 0
        a1 = Adresse(pobox=pobox, strasse=l[8], plz=l[9], ort=l[10], country=land)
        a2 = Adresse(pobox=pobox, strasse=l[8], plz=l[9], ort=l[10], country=land)
        a3 = Adresse(pobox=pobox, strasse=l[8], plz=l[9], ort=l[10], country=land)
        a1.save()
        a2.save()
        a3.save()

        mm=VereinsMitglied(mitgliedsnummer=int(mnr),
                   username=username,
                   anrede=anr,
                   titel=t,
                   namenszusatz= "{} {}".format(l[5], l[6]),
                   tel=l[12],
                   fax=l[13],
                   beigz=l[14],
                   beidat=beidat,
                   storndat=storndat,
                   mitgliedsart=m,
                   kostenart=k,
                   versand=v,
                   gebdat=gebdat,
                   sub=l[23],
                   vortragold=l[26],
                   berufsgruppe=b,
                   heftanzahl=int(heftanz),
                   first_name=l[3],
                   last_name=l[4],
                   wohnadresse=a1,
                   lieferadresse=a2,
                   rechnungsadresse=a3
        )
        mm.save()
    
    df = pd.read_csv('mitglieder/olddb/MITGLIEDER_01.csv',delimiter=';',encoding="utf-8", error_bad_lines=False)
    df=df.fillna('')
    for i,r in df.iterrows():
        if r['Geboren']:
            gebdat=dt.strptime(r['Geboren'],'%m/%d/%Y').strftime('%Y-%m-%d')
        else:
            gebdat=None

        if r['BEIDAT']:
            beidat=dt.strptime(r['BEIDAT'],'%m/%d/%Y').strftime('%Y-%m-%d')
        else:
            beidat=None

        if r['STORNODAT']:
            storndat=dt.strptime(r['STORNODAT'],'%m/%d/%Y').strftime('%Y-%m-%d')
        else:
            storndat=None

        t = None
        if r['Titel']:
            tit = Titel.objects.filter(oldid=int(r['Titel']))
            if tit:
                t = tit.first().titel

        k = None
        if r['Kost']:
            k = Kosten.objects.get(art=r['Kost'])

        b = None
        if r['Beruf']: 
            b = Beruf.objects.get(oldid=int(r['Beruf']))

        anr = None
        if r['Anrede']:
            anr = Anrede.objects.get(oldid=int(r['Anrede'])).anrede

        v = None
        if r['Versand']:
            v = Versand.objects.get(versand=r['Versand']).bezeichnung

        m = None
        if r['Mitart']:
            m = Mitgliedsart.objects.get(mitart=r['Mitart'])

        l = None
        if r['Land']:
            l = Land.objects.get(oldid=int(r['Land']) )

        heftanzahl = None
        if r['Heftanzahl']:
            heftanzahl = int(r['Heftanzahl'])

        pobox = None
        if r['POBOX']:
           pobox = r['POBOX'] 

        print("{} {} {} {} {}".format(r['POBOX'], r['Strasse'], r['PLZ'], r['Ort'], l))
        a1 = Adresse(pobox=pobox, strasse=r['Strasse'], plz=r['PLZ'], ort=r['Ort'], country=l )
        a2 = Adresse(pobox=pobox, strasse=r['Strasse'], plz=r['PLZ'], ort=r['Ort'], country=l )
        a3 = Adresse(pobox=pobox, strasse=r['Strasse'], plz=r['PLZ'], ort=r['Ort'], country=l )
        a1.save()
        a2.save()
        a3.save()
        if r['mail']:
            username = r['mail']
            if VereinsMitglied.objects.filter(username=username):
                username+='1'
        else:
            username = "{}{}{}".format(r['Mitgliednummer'], r['Vorname'], r['Name1'])

        mm=VereinsMitglied(mitgliedsnummer=int(r['Mitgliednummer']),
                   username=username,
                   anrede=anr,
                   titel=t,
                   namenszusatz= "{} {}".format(r['Name2'], r['Name3']),
                   tel=r['Tel'],
                   fax=r['Fax'],
                   beigz=r['BEIGZ'],
                   beidat=beidat,
                   storndat=storndat,
                   mitgliedsart=m,
                   kostenart=k,
                   versand=v,
                   gebdat=gebdat,
                   sub=r['SUB'],
                   vortragold=r['Vortrag'],
                   berufsgruppe=b,
                   heftanzahl=heftanzahl,
                   first_name=r['Vorname'],
                   last_name=r['Name1'],
                   email=r['mail'],
                   anmerkung=r['Anmerkung'],
                   wohnadresse=a1,
                   lieferadresse=a2,
                   rechnungsadresse=a3
                )
        mm.save()
    VereinsMitglied.objects.filter(anrede="nan").update(anrede="")
    VereinsMitglied.objects.filter(beigz=0).update(beigz="")
    VereinsMitglied.objects.filter(fax=0).update(fax="")
    VereinsMitglied.objects.filter(first_name=0).update(first_name="")
    VereinsMitglied.objects.filter(email=0).update(email="")
    VereinsMitglied.objects.filter(tel=0).update(tel="")



    df = pd.read_csv('mitglieder/olddb/OP.txt',delimiter=';',encoding="latin-1")
    for i,x in df.iterrows():
        m=VereinsMitglied.objects.filter(mitgliedsnummer=x[0]).first()
        if m:
            try:
                erstellt=dt.strptime(x[1],'%d.%m.%Y %H:%M:%S')
            except:
                erstellt=dt(2000,1,1)
            o=offenePosten(mitglied=m,
                        erstellt=erstellt,
                        bezahltam=dt.strptime(x[2],'%d.%m.%Y %H:%M:%S'),
                        offen=float(x[3].replace(',','.')),
                        zahlung=float(x[4].replace(',','.')),
                        description=x[5],
                        bezahlt=x[6]
                        ).save()

    v=Vortragsort(Vortragsort='Wien')
    v.save()
    v=Vortragsort(Vortragsort='Graz')
    v.save()
    v=Vortragsort(Vortragsort='Linz')
    v.save()
    v=Vortragsort(Vortragsort='Innsbruck')
    v.save()
    for m in VereinsMitglied.objects.all():
        if m.vortragold == '': m.vortragold=0
        k=int(float(m.vortragold))
        if k>0:
            s = Vortragold.objects.get(oldid=int(float(m.vortragold))).Vortragsort
            if 'W' in s:
                v = Vortragsort.objects.get(Vortragsort='Wien')
                m.vortrag.add(v)
            if 'G' in s:
                v = Vortragsort.objects.get(Vortragsort='Graz')
                m.vortrag.add(v)
            if 'L' in s:
                v = Vortragsort.objects.get(Vortragsort='Linz')
                m.vortrag.add(v)
            if 'I' in s:
                v = Vortragsort.objects.get(Vortragsort='Innsbruck')
                m.vortrag.add(v)
        m.save()

    # Institutionen anlegen
    for v in VereinsMitglied.objects.filter(first_name=''):
        inst = Institution(institution_name=v.last_name, mitgliedsnummer=v.mitgliedsnummer,
            name2=v.namenszusatz, tel=v.tel, fax=v.fax,
            beigz=v.beigz, beidat=v.beidat, storndat=v.storndat, mitgliedsart=v.mitgliedsart,
            kostenart=v.kostenart, versand=v.versand, sub=v.sub,
            berufsgruppe=v.berufsgruppe, heftanzahl=v.heftanzahl, anmerkung=v.anmerkung,
            wohnadresse=v.wohnadresse, lieferadresse=v.lieferadresse,
            rechnungsadresse=v.rechnungsadresse, dsgvo=v.dsgvo, email=v.email)
        inst.save()
        inst.vortrag.set(v.vortrag.all())
        v.offeneposten_set.all().delete()
        v.delete()


def parse_date_time(x):
    dat=None
    if x != '': 
        dat=dt.strptime(x,'%d.%m.%Y %H:%M:%S').strftime('%Y-%m-%d')
    return dat


def import_abodb():
    f = codecs.open('mitglieder/abodb/LAND.txt', 'r', 'utf-8')
    ll = f.readlines()[1:]
    f.close()
    for line in ll:
        r = line.replace("\r\n","").split(";")
        l,c = Land.objects.get_or_create(land=r[1], defaults={'iso':r[2],'EU':r[3], 'oldid':r[0]})
    laender = [l.replace('\r\n','').split(";") for l in ll]

    f = codecs.open('mitglieder/abodb/ANREDE.txt', 'r', 'utf-8')
    ll = f.readlines()[1:]
    f.close()
    anrede = [l.replace('\r\n','').split(";") for l in ll]

    f = codecs.open('mitglieder/abodb/TITEL.txt', 'r', 'utf-8')
    ll = f.readlines()[1:]
    f.close()
    titel = [l.replace('\r\n','').split(";") for l in ll]


    AboHeft.objects.all().delete()
    Abonnent.objects.all().delete()
    f = codecs.open('mitglieder/abodb/ABONNENT.txt', 'r', 'utf-8')
    ll = f.readlines()[1:]
    f.close()

    for line in ll:
        l = line.replace("\r\n","").split(';')
        print(l)

        #daten werden nur eingelesen wenn es einen ort gibt
        if l[10] != '':
            if l[3] != '':
                namen = "{} {}".format(l[3],l[4])
            else:
                namen = l[4]

            land = [v for i,v in enumerate(laender) if v[0]==l[17]][0][1]
            print(land)

            pobox = l[7]
            if l[7] == '' : pobox=0
            adresse = Adresse(pobox=pobox, strasse=l[8], plz=l[9], ort=l[10], country=Land.objects.get(land=land))
            adresse.save()
            abonnent = Abonnent(kundennummer = l[0], titel=l[2], name=namen,
                name2=l[5], name3=l[6], tel=l[11], fax=l[12], uid=l[13],
                prozent=l[14].replace(',','.'), rechnungsanzahl=l[15], email=l[18],
                rechnungsanschrift=adresse)

            abonnent.save()
    
    # 0: AboNummer
    # 1: KundenNummer
    # 3: Anrede
    # 4: Titel
    # 5: Vorname
    # 6: nachname-1
    # 7: name2
    # 8: name3
    # 9: PO-BOX
    # 10: Strasse
    # 11: PLZ
    # 12: Ort
    # 13: Tel
    # 14: Fax
    # 15: Heftanzahl
    # 16: BEIGZ
    # 17: BEIDAT
    # 18: STORNODAT
    # 19: ABOART
    # 20: Land
    # 21: Rückstand
    # 22: Gutschrift
    # 23: ABOAnfang
    # 24: ABOEnde
    # 25: Anmerkung

    #import aboheft
    AboHeft.objects.all().delete()
    f = codecs.open('mitglieder/abodb/ABOHEFT.txt', 'r', 'utf-8')
    ll = f.readlines()[1:]
    f.close()

    nonarr=[]

    for line in ll:
        l = line.replace("\r\n","").split(';')
        print(l)

        #daten werden nur eingelesen wenn es einen ort gibt
        if l[12] != '':
            if l[4] not in ['0', '']:
                tit = [v for i,v in enumerate(titel) if v[0]==l[4]][0][1]
            else:
                tit = ''

            if l[3] != '0':
                anr = [v for i,v in enumerate(anrede) if v[0]==l[3]][0][1]
            else:
                anr = ''

            beidat = parse_date_time(l[17])
            storndat = parse_date_time(l[18])
            aboanfang = parse_date_time(l[23])
            aboende = parse_date_time(l[24])
            
            
            land = [v for i,v in enumerate(laender) if v[0]==l[20]][0][1]
            pobox = l[9]
            if l[9] == '' : pobox=0

            abon = Abonnent.objects.filter(kundennummer=l[1])
            if abon:
                abon = abon[0]
                
                abo = AboHeft(abonummer = l[0], kundennummer = abon, anrede = anr, titel = tit, 
                            vorname = l[5], nachname = l[6], surname2 = l[7], surname3 = l[8], tel = l[13],
                            fax = l[14], heftanzahl = l[15], beigz = l[16], beidat = beidat, storndat = storndat,
                            aboart=l[19], rueckstand = l[21].replace(',','.'), gutschrift = l[22].replace(',','.'), aboanfang = aboanfang, aboende = aboende,
                            anmerkung = l[25], pobox=pobox, strasse=l[10], plz=l[11], ort=l[12], country=Land.objects.get(land=land))
                abo.save()
            else:
                nonarr.append(l[0])
        else:
            nonarr.append(l[0])
    print(nonarr)
            