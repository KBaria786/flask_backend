from flask import current_app, Blueprint, render_template, request
import os
from werkzeug.utils import secure_filename
from ..exceptions import InvalidRequestException
from ..services import pdf_services, atlas_services
from datetime import datetime

from pypdf import PdfReader, PdfWriter

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")

@main_bp.route("/upload", methods=["POST"])
def upload():

    file = None
    filename = ""
    allowed_extensions = ["pdf"]
    pages = []
    proccessed_pages = []
    file_errors = {}
    
    # check if file is present
    if "file" not in request.files or request.files.get("file").filename == "":
        file_errors["file"] = ["File is required."]
    else:
        file = request.files.get("file")
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit(".", 1)[1].lower()

        # check if file has valid format
        if file_extension not in allowed_extensions:
            file_errors["file"] = ["Invalid file format. Only PDF files are accepted."]
        else:
            # check if pdf has >= 3 pages
            pages = pdf_services.get_pages(file)
            proccessed_pages = pages
            if len(pages) < 3:
                file_errors["file"] = ["Invalid file content. The PDF must contain at least 3 pages."]
            
    # raise invalid request exception if file errors are present
    if file_errors:
        raise InvalidRequestException(messages = {**file_errors})

    # form data
    mask_aadhaar = request.form.get("mask_aadhaar")
    add_watermark = request.form.get("add_watermark")
    compare_faces = request.form.get("compare_faces")
    compress_pdf = request.form.get("compress_pdf")

    timestamp = int(datetime.now().timestamp() * 1000)

    if mask_aadhaar == "on":
        # save second page of pdf file
        aadhaar_file_name = f"{filename.rsplit(".", 1)[0]}_aadhaar.pdf"
        save_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER"), str(timestamp))
        pdf_services.save_pdf_pages([pages.pop(1)], aadhaar_file_name, save_directory)

        # send aadhaar mask request to atlas
        aadhaar_file_directory = os.path.join(save_directory, aadhaar_file_name)
        with open(aadhaar_file_directory, "r") as aadhaar_file:
            response = atlas_services.mask_aadhaar(aadhaar_file)

            if response.status_code == 200:
                # logic to add file at index
                aadhaar_pdf_reader = PdfReader(aadhaar_file)
                masked_aadhaar_page = aadhaar_pdf_reader.pages[1]

                proccessed_pages.insert(1, masked_aadhaar_page)

        # more exception handling needed
        