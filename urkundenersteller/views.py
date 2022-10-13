from django.contrib import messages
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

import chardet

from urkundenersteller import logic
from urkundenersteller.models import Certificate


# Create your views here.
def index(request: HttpRequest):
    return HttpResponse("This is the index")


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