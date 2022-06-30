def generate_file(note_imposition_payment):
    if not note_imposition_payment.note_payment:
        return False

    # WeasyPrint
    from weasyprint import HTML, CSS
    from weasyprint.fonts import FontConfiguration
    from weasyprint.pdf import PDFFile, pdf_format

    # Pdf rendering
    pdf_str_rendered = render_to_string(
        "gdaf/noteimposition_bordereau.html",
        {
            "noteimposition": note_imposition_payment.note_imposition,
            "noteimposition_payment": note_imposition_payment.note_payment,
            "statement": note_imposition_payment,
        },
    )
    file_django = "bordereau_%s_%s.pdf" % (
        note_imposition_payment.note_imposition.reference,
        note_imposition_payment.pk,
    )

    # font_config = FontConfiguration()
    html = HTML(string=pdf_str_rendered)
    # css = CSS(
    #     string="""
    #     @font-face {
    #         font-family: Gentium;
    #         src: url(http://example.com/fonts/Gentium.otf);
    #     }
    #     h1 { font-family: Gentium }""",
    #     font_config=font_config,
    # )
    # html.write_pdf("/tmp/example.pdf", stylesheets=[css], font_config=font_config)
    content = io.BytesIO(html.write_pdf())

    pdf_file = PDFFile(content)
    # params = pdf_format('/OpenAction [0 /FitV null]')
    # pdf_file.extend_dict(pdf_file.catalog, params)
    # pdf_file.finish()
    # pdf = pdf_file.fileobj.getvalue()
    # open('/tmp/weasyprint.pdf', 'wb').write(pdf)

    note_imposition_payment.note_imposition.paiement_externe_file.save(
        file_django, ContentFile(content.getvalue())
    )
    note_imposition_payment.note_imposition.save()

    # print(
    #     content, content.getvalue(), note_imposition_payment.note_imposition.paiement_externe_file
    # )

    note_imposition_payment.fichier_paiement.save(
        file_django, ContentFile(content.getvalue())
    )
    note_imposition_payment.printed = True
    note_imposition_payment.save()

    # Close Buffer
    content.close()

    return True
