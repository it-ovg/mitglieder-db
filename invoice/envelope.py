#!/bin/python3

import os

from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from . import settings as s
from . import utils as u


DEFAULT_SENDER = {
    "sender_name": "VGI",
    "sender_extra": None,
    "sender_street": "Schiffamtsgasse 1-3",
    "sender_zip": "1020",
    "sender_city": "Wien",
}


def create_envelope(**kwargs):
    """ Create multi purpose envelope """

    margin_top = 0.75*cm
    margin_right = 0.75*cm
    margin_left = 0.75*cm
    margin_bottom = 0.75*cm

    env_width = 10*cm
    env_height = 6*cm

    logo_height = 1.8*cm

    rowHeights = 13

    envelope_type = kwargs.get("type", "any")
    recipient_id = kwargs.get("recipient_id")
    recipient_name = kwargs.get("recipient_name")
    recipient_extra = kwargs.get("recipient_extra", "")
    recipient_street = kwargs.get("recipient_street")
    recipient_zip = kwargs.get("recipient_zip")
    recipient_city = kwargs.get("recipient_city")
    recipient_country = kwargs.get("recipient_country", "")

    sender_name = kwargs.get("sender_name")
    sender_extra = kwargs.get("sender_extra", "")
    sender_street = kwargs.get("sender_street")
    sender_zip = kwargs.get("sender_zip")
    sender_city = kwargs.get("sender_city")
    sender_country = kwargs.get("sender_country", "").upper()

    sender_logo = kwargs.get("sender_logo", "eco_post.png")

    generate_pdf = kwargs.get("generate_pdf", False)
    
    envelope_basename = "ovg_env_{}_{}".format(envelope_type, recipient_id)
    envelope_filename = os.path.join(s.OUT_DIR, "{}.pdf".format(envelope_basename))
    buffer = BytesIO()

    canvas_out = envelope_filename if generate_pdf else buffer

    canvas = Canvas(
        canvas_out,
        pagesize=landscape((env_height, env_width))
    )

    print("Writing Canvas to %s" % canvas_out)

    # Add postal logo
    postal_logo_path = str(os.path.join(s.ROOT_DIR, s.TEMPLATE_DIR, sender_logo))
    postal_logo = u.get_image(postal_logo_path, logo_height)
    w, h = postal_logo.wrapOn(canvas, 0, 0)
    print(w, h)

    postal_logo.drawOn(canvas, x=env_width - w - margin_right, y=env_height - h - margin_top)

    # Add sender
    sender_meta_data = [
        ["{}, {}".format(sender_name, sender_street), " "],
        ["{} {}".format(sender_zip, sender_city), ""],
    ]
    sender_meta_table = Table(data=sender_meta_data, rowHeights=rowHeights)
    sender_meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    w, h = sender_meta_table.wrapOn(canvas, 0, 0)
    sender_meta_table.drawOn(canvas, 0.75*cm, env_height - h - margin_top)

    # Add recipient
    recipient_meta_data = [
        [recipient_name, ""]
    ]

    if recipient_extra:
        recipient_meta_data.append(
            [recipient_extra, ""],
        )
    recipient_meta_data += [
        [recipient_street, ""],
        ["{} {}".format(recipient_zip, recipient_city), ""]
    ]
    if recipient_country:
        recipient_meta_data.append(
            [recipient_country.upper(), ""]
        )
    recipient_meta_table = Table(data=recipient_meta_data, rowHeights=rowHeights)
    recipient_meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    w, h = recipient_meta_table.wrapOn(canvas, 0, 0)
    print("Recipient Size")
    print(w, h)
    recipient_meta_table.drawOn(canvas, margin_left, margin_bottom)

    # Generate Output
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def create_envelope_int(**kwargs):
    """ Create envelope for EU and Abroad usage """
    d = {
        "recipient_name": kwargs.get("recipient_name"),
        "recipient_extra": kwargs.get("recipient_extra", ""),
        "recipient_street": kwargs.get("recipient_street"),
        "recipient_zip": kwargs.get("recipient_zip"),
        "recipient_city": kwargs.get("recipient_city"),
        "recipient_country": kwargs.get("recipient_country"),
        "type": "int",
    }
    kwargs.update(d)
    kwargs.update(DEFAULT_SENDER)
    return create_envelope(**kwargs)


def create_envelope_aut(**kwargs):
    """ Create envelope for Austria """
    d = {
        "recipient_name": kwargs.get("recipient_name"),
        "recipient_extra": kwargs.get("recipient_extra", ""),
        "recipient_street": kwargs.get("recipient_street"),
        "recipient_zip": kwargs.get("recipient_zip"),
        "recipient_city": kwargs.get("recipient_city"),
        "type": "aut",
    }
    kwargs.update(d)
    kwargs.update(DEFAULT_SENDER)
    return create_envelope(**kwargs)


def create_envelope_bev(**kwargs):
    """ Create envelope for internal usage """
    d = {
        "recipient_name": kwargs.get("recipient_name"),
        "recipient_extra": kwargs.get("recipient_extra"),
        "recipient_street": kwargs.get("recipient_street", "Schiffamtsgasse 1-3"),
        "recipient_zip": kwargs.get("recipient_zip", "1020"),
        "recipient_city": kwargs.get("recipient_city", "Wien"),
        "type": "bev",
        "sender_logo": "OVG_RGB.jpg",
    }
    kwargs.update(d)
    kwargs.update({
        "sender_name": "VGI",
        "sender_street": "Interne Zustellung",
        "sender_zip": "",
        "sender_city": ""
    })
    return create_envelope(**kwargs)


if __name__ == "__main__":
    create_envelope_aut(
        recipient_id="108",
        recipient_name="Dipl.-Ing. Jürgen Fredriksson",
        recipient_street="Steingrubenweg 4k",
        recipient_zip="2352",
        recipient_city="Gumpoldskirchen",
        generate_pdf=True
    )

    create_envelope_int(
        recipient_id="108",
        recipient_name="Dipl.-Ing. Jürgen Fredriksson",
        recipient_extra="Messfuchs",
        recipient_street="Steingrubenweg 4k",
        recipient_zip="2352",
        recipient_city="Gumpoldskirchen",
        recipient_country="Austria",
        generate_pdf=True
    )

    create_envelope_bev(
        recipient_id="108",
        recipient_name="Dipl.-Ing. Jürgen Fredriksson",
        recipient_extra="Abt. V1",
        generate_pdf=True
    )

