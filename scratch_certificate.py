
!pip install PyPDF2

!pip install reportlab

import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import fonts
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def overlay_text_on_template(template_path, names, output_directory):
    for name in names:
        template = PdfReader(open(template_path, 'rb'))

        # Append a timestamp to ensure unique file names
        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_path = f"{output_directory}/{name}_{timestamp}_certificate.pdf"
        output = PdfWriter()

        # Create a canvas to overlay text
        packet = BytesIO()

        # Use landscape orientation for the canvas (adjust as needed)
        can = canvas.Canvas(packet, pagesize=landscape(letter))

        # Set the font size (adjust as needed)
        font_size = 50

        # Use the Arial font (if available)
        try:
            can.setFont("Times-Roman",font_size)
        except:
            # If Arial is not available, use a default font
            can.setFont("Helvetica", font_size)

        # Get the page size
        page_width, page_height = landscape(letter)

        # Calculate the center coordinates for horizontal and vertical alignment
        text = name
        text_width = can.stringWidth(text)
        text_height = font_size
        text_x = ((page_width - text_width) / 2) + 24
        text_y = ((page_height - text_height) / 2) + 16

        # Draw the text at the center
        can.drawString(text_x, text_y, text)

        can.save()
        packet.seek(0)

        overlay = PdfReader(packet)
        template_page = template.pages[0]
        template_page.merge_page(overlay.pages[0])
        output.add_page(template_page)

        # Print the output filename for debugging
        print("Output Filename:", output_path)

        # Save the overlaid certificate as a new PDF file
        with open(output_path, 'wb') as output_file:
            output.write(output_file)

        # Close the output file to prevent overwriting and ensure proper closing
        output_file.close()

        # Introduce a delay of 1 second between iterations
        time.sleep(1)

names = ["John Doe", "Jane Smith","Muhammad Burhanuddin"]
template_path = "input_certificate.pdf"  # Use the actual filename here
output_directory = "output_certificates"

overlay_text_on_template(template_path, names, output_directory)