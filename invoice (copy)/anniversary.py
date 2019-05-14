#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import qrcode
import qrcode.image.svg

from svglib.svglib import svg2rlg
from io import BytesIO

from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from invoice import settings as s
from invoice import utils as u


def create_anniversary(**kwargs):
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
    styles = getSampleStyleSheet()
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(s.ROOT_DIR, s.TEMPLATE_DIR))
    template_env = jinja2.Environment(loader=template_loader)
    TEMPLATE_FILE = "anniversary.txt.j2"
    template = template_env.get_template(TEMPLATE_FILE)

    # Outputoption
    generate_pdf = kwargs.get("generate_pdf", False)

    # Jubiläumsinfo
    customer_id = kwargs.get("customer_id")
    customer_anniversary = kwargs.get("customer_anniversary")
    customer_salutation = kwargs.get("customer_salutation", None)
    customer_name = kwargs.get("customer_name")

    # Lieferanschrift
    letter_street = kwargs.get("letter_street")
    letter_zip = kwargs.get("letter_zip")
    letter_city = kwargs.get("letter_city")
    letter_country = kwargs.get("letter_country", "AUT")

    letter_date_str = kwargs.get("letter_date", datetime.date.today().strftime(s.ISO_DATE))
    letter_date = datetime.datetime.strptime(letter_date_str, s.ISO_DATE)
    letter_deadline = letter_date + datetime.timedelta(days=30*6)
    letter_reference = kwargs.get("letter_reference", "{}/{}".format(letter_date.year, customer_anniversary))
    
    letter_basename = "ovg_anniversary_{}_{:03d}".format(customer_id, customer_anniversary)
    letter_filename = os.path.join(s.OUT_DIR, "{}.pdf".format(letter_basename))

    margin_left = 2.0*cm
    margin_left_text = 2.0*cm
    margin_right = 2.0*cm

    buffer = BytesIO()
    canvas = Canvas(
        letter_filename if generate_pdf else buffer,
        pagesize=portrait(A4)
    )

    # OVG Header
    u.generate_header(canvas, pos_y=s.A4_HEIGHT-1*cm, pos_x=s.A4_WIDTH/2+4.7*cm)
    u.generate_member_meta(canvas=canvas, invoice_reference='blabla',
        member_id = customer_id, 
        invoice_date_str=letter_date.strftime(s.ISO_DATE), 
        pos_y=s.A4_HEIGHT-2.4*cm, 
        pos_x=s.A4_WIDTH/2+4.7*cm)

    # Rechnungsanschrift
    u.generate_address(canvas, 
        description=customer_salutation,
        name=customer_name,
        street=letter_street, 
        zip_code=letter_zip, 
        city=letter_city, 
        country=letter_country,
        pos_x=margin_left, pos_y=s.A4_HEIGHT-5.4*cm)

    # Subject
    subject_text = "Herzlichen Glückwunsch!"
    p = Paragraph(subject_text, styles["Heading3"])
    used_width1, used_height1 = p.wrap(s.A4_WIDTH - margin_left_text - margin_right, 0*cm)
    line_widths = p.getActualLineWidths0()
    nol = len(line_widths)
    if nol > 1:
        actual_width1 = used_width1
    elif nol == 1:
        actual_width1 = min(line_widths)
    else:
        return 0, 0
    p.drawOn(canvas, margin_left_text, s.A4_HEIGHT - 11.5*cm)

    # Letter Text
    letter_text = template.render(
        anniversary=customer_anniversary,
    )
    p = Paragraph(letter_text, styles["Normal"])
    used_width2, used_height2 = p.wrap(s.A4_WIDTH-margin_left_text-margin_right, 0)
    line_widths = p.getActualLineWidths0()
    nol = len(line_widths)
    if nol > 1:
        actual_width2 = used_width2
    elif nol == 1:
        actual_width2 = min(line_widths)
    else:
        return 0, 0
    p.drawOn(canvas, margin_left_text, s.A4_HEIGHT-16.0*cm)

    # OVG-President
    salute_president = "Dipl.-Ing. Julius Ernst<br/>(Präsident)"
    p = Paragraph(salute_president, styles["Normal"])
    used_width3, used_height3 = p.wrap(s.A4_WIDTH-margin_left_text-margin_right, 0)
    line_widths = p.getActualLineWidths0()
    nol = len(line_widths)
    if nol > 1:
        actual_width3 = used_width3
    elif nol == 1:
        actual_width3 = min(line_widths)
    else:
        return 0, 0
    p.drawOn(canvas, margin_left_text, s.A4_HEIGHT-16.0*cm - used_height2 - 2*cm)

    # OVG-Generalsekretär
    salute_secretary = "Dipl.-Ing. Franz Blauensteiner<br/>(Generalsekretär)"
    p = Paragraph(salute_secretary, styles["Normal"])
    used_width4, used_height4 = p.wrap(s.A4_WIDTH-margin_left_text-margin_right, 0)
    line_widths = p.getActualLineWidths0()
    nol = len(line_widths)
    if nol > 1:
        actual_width4 = used_width4
    elif nol == 1:
        actual_width4 = min(line_widths)
    else:
        return 0, 0
    p.drawOn(canvas, s.A4_WIDTH/2, s.A4_HEIGHT-16.0*cm - used_height2 - 2*cm)

    # OVG Footer
    footer_data = [
        ["OVG - Herausgeber der einzigen Zeitschrift für Vermessung und Geoinformation in Österreich"],
        ["Bank", s.BANK, "Web", s.OVG_SITE],
        ["BIC", s.BIC, "", ""],
        ["IBAN", s.IBAN_NUMBER, "ZVR-Zahl", s.OVG_ZVR]
    ]
    print("W: {}")
    footer_table = Table(data=footer_data, colWidths=[1*cm, 12.5*cm, 1.5*cm, 2*cm], rowHeights=12)
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), "TOP"),
        ('SPAN', (0, 0), (3, 0)),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
    ]))
    w1, h1 = footer_table.wrapOn(canvas, 0, 0)
    footer_table.drawOn(canvas, margin_left, 1*cm)

    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


if __name__ == "__main__":
    create_anniversary(
        letter_date="2019-11-22",
        letter_street="Schiffamtsgasse 1-3", 
        letter_zip="1020", 
        letter_city="Wien",
        letter_country="AUT",
        customer_name="DI Jürgen Fredriksson",
        customer_id=108,
        customer_salutation="Herr",
        customer_anniversary=75,
        generate_pdf=True
    )