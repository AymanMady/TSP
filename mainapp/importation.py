from django.shortcuts import render
import networkx as nx
from geopy.distance import geodesic
# from .graph import *
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import openpyxl

def importation(request):
    if request.method == "POST" and request.FILES["excel_file"]:
        excel_file = request.FILES["excel_file"]
        file_path = os.path.join(settings.MEDIA_ROOT, 'data.xlsx')
            # Delete data.xlsx if it exists

        try:
            os.remove('files/data.xlsx')
            print("File deleted successfully")
        except FileNotFoundError:
            print("File does not exist")
        fs = FileSystemStorage()
        filename = fs.save("files/data.xlsx", excel_file)
        uploaded_file_url = fs.url(filename)
        return render(request, "importation.html", {"uploaded_file_url": uploaded_file_url})
    return render(request, "importation.html")



 