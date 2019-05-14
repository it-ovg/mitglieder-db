#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import qrcode
import qrcode.image.svg

from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, Paragraph
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from . import settings as s


def generate_qr(payload):
    factory = qrcode.image.svg.SvgImage
    return qrcode.make(payload, image_factory=factory)


def generate_header(canvas, pos_x=10*cm, pos_y=s.A4_WIDTH-1*cm):

    # OVG Header
    styles = getSampleStyleSheet()

    pos_y2 = pos_y-2*cm  # 18 cm
    pos_y1 = pos_y-1*cm  # 19 cm

    ovg_logo = ImageReader(os.path.join(s.ROOT_DIR, s.TEMPLATE_DIR, "OVG_RGB.jpg"))
    canvas.drawImage(ovg_logo, x=1*cm, y=pos_y2, height=2*cm, width=2*cm)

    ovg_meta_data = [
        ["Schiffamtsgasse 1-3", " "],
        ["1020 Wien", ""],
        ["Austria", ""],
        ["Tel: +43 (1) 21110 822711"],
        ["E-Mail: office@ovg.at"],
    ]
    ovg_meta_table = Table(data=ovg_meta_data, rowHeights=12)
    w, h = ovg_meta_table.wrapOn(canvas, 0, 0)
    ovg_meta_table.drawOn(canvas, pos_x, pos_y-h)

    header_de_style = styles["Title"]
    header_de_style.alignment = TA_LEFT
    header_de_style.fontSize = 11.5
    header_de_style.leading = 11.5 + 4
    header_de_style.borderPadding = 5

    header_de = Paragraph("Österreichische Gesellschaft für Vermessung und Geoinformation", header_de_style)
    header_en = Paragraph("Austrian Society for<br />Surveying and Geoinformation", styles["Normal"])
    h, w = header_de.wrap(7*cm, 1.2*cm)
    header_de.drawOn(canvas, 3*cm + 0.3*cm, pos_y1)
    h, w = header_en.wrap(7*cm, 1.2*cm)
    header_en.drawOn(canvas, 3*cm + 0.3*cm, pos_y2)


def generate_address(canvas, pos_x, pos_y,
    description=None,
    company=None, department=None,
    name="Max Musermann",
    street="Kaiserstraße 1", zip_code="1160", city="Wien", country=None):
    data = []
    if description:
        data += [[description, ""]]
    if company:
        data += [[company, ""]]
        if department:
            data += [[department, ""]]
    if name:
        data += [[name, ""]]
    data += [
        [street, ""],
        ["{} {}".format(zip_code, city), ""],
    ]
    if country:
        data += [[country, ""]]
    table = Table(data=data, rowHeights=12)
    w, h = table.wrapOn(canvas, 0, 0)
    table.drawOn(canvas, pos_x, pos_y-h)


def generate_member_meta(canvas, 
    invoice_date_str, 
    invoice_reference, 
    member_id,
    vat_id=None,
    pos_x=10*cm, 
    pos_y=s.A4_WIDTH-1*cm):

    pos_y3 = pos_y - 3*cm
    
    # Member Meta
    member_meta_data = [
        ["Datum", invoice_date_str],
        ["Rechnungsnr.", invoice_reference],
        ["Kundennr.", member_id]
    ]
    if vat_id:
        member_meta_data += [["Ihre UID", vat_id]]
    # row_height = 0.5*cm
    member_meta_table = Table(data=member_meta_data, rowHeights=12)
    w, h = member_meta_table.wrapOn(canvas, 0, 0)
    member_meta_table.drawOn(canvas, pos_x, pos_y3-h)
