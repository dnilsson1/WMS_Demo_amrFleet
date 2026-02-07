from io import BytesIO

from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_label_pdf(product_sku):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 720, "Product Label")

    c.setFont("Helvetica", 14)
    c.drawString(72, 690, f"SKU: {product_sku}")

    barcode = code128.Code128(product_sku, barHeight=60, barWidth=1.2)
    barcode.drawOn(c, 72, 600)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
