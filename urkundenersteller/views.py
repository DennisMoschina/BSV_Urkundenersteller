from datetime import datetime

from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from urkundenersteller import logic
from urkundenersteller.logic import create_pdf_from_certificate
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
    create_pdf_from_certificate(certificates[0])

    return render(request, template, {"certificates": certificates})


def upload_winner_csv(request: HttpRequest):
    template: str = "upload_csv.html"

    if request.method == "GET":
        return render(request, template)

    print(f"files: {request.FILES}")
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

    context = {}
    return render(request, template, context)