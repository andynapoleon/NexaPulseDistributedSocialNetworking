from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os

def index(request):
    return render(request, 'index.html')

def public(request, path):
    path = os.path.join(settings.BASE_DIR, "client/dist/" + path)
    with open(path, 'rb') as f:
        image_data = f.read()
    response = HttpResponse(image_data, content_type='image/png')
    return response


def assets(request, path):
    # Construct the absolute path to the requested file
    file_path = os.path.join(settings.BASE_DIR, "client/dist/assets", path)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return HttpResponse(status=404)
    
    # Determine the content type based on the file extension
    content_type = None
    if path.endswith('.js'):
        content_type = 'application/javascript'
    elif path.endswith('.css'):
        content_type = 'text/css'

    # Serve the file using FileResponse
    return FileResponse(open(file_path, 'rb'), content_type=content_type)

    