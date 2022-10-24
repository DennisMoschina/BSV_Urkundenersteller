import io
import os.path
from datetime import datetime

import numpy as np
from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile
from django.http import FileResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from urkundenersteller import logic
from urkundenersteller.logic import create_certificates_as_pdf
from urkundenersteller.logic import create_pdf_from_certificate
from urkundenersteller.logic import save_as_pdf
from urkundenersteller.models import Certificate


# Create your views here.
def index(request: HttpRequest):
    template: str = "index.html"

    if request.method == "GET":
        return render(request, template)

    data: dict = request.POST.dict()
    club_name: str = data["club_name"]
    tournament_name: str = data["tournament_name"]
    tournament_date_str: str = data["date"]

    club_name = club_name if club_name != '' else "BSV Eggenstein-Leopoldshafen"
    date: datetime = datetime.strptime(tournament_date_str, "%Y-%m-%d") if tournament_date_str != ''\
        else datetime.now()

    logic.create_tournament(tournament_name, date, club_name)

    csv_file: UploadedFile = request.FILES["file"]
    print(f"csv_file: {csv_file}")
    print(f"size: {csv_file.size}")
    assert isinstance(csv_file, UploadedFile)

    if not (csv_file.name.endswith('.csv') or csv_file.name.endswith('.CSV')):
        print("File is not a CSV file")
        messages.error(request, 'This is not a csv file')
        return render(request, template)

    read_file = csv_file.read()
    certificates: list[Certificate] = logic.parse_winner_input(read_file)

    certificates_buffer: io.BytesIO = create_certificates_as_pdf(certificates)

    save_as_pdf(certificates_buffer, "out/urkunden.pdf")
    certificates_buffer.seek(0)

    return redirect("urkunden")


def previously_created_certificates(request: HttpRequest):
    if os.path.exists("out/urkunden.pdf"):
        with open("out/urkunden.pdf", "rb") as f:
            return FileResponse(io.BytesIO(f.read()), as_attachment=False, filename="urkunden.pdf")
    else:
        return HttpResponse("Bisher wurden keine Urkunden erstellt.")
