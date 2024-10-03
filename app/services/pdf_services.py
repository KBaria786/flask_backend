from pypdf import PdfReader, PdfWriter
import os

# get all pages of pdf
def get_pages(pdf_file):
    reader = PdfReader(pdf_file)

    pages = []
    for page in reader.pages:
        pages.append(page)

    return pages

# save pdf pages as file
def save_pdf_pages(pages, filename, directory):
    if pages:
        writer = PdfWriter()

        for page in pages:
            writer.add_page(page)

        os.makedirs(directory, exist_ok = True)
        save_directory = os.path.join(directory, filename)

        with open(save_directory, "wb") as output_file:
            writer.write(output_file)