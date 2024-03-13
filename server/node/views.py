from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


# Create your views here.
@api_view(("GET",))
def test(request):
    # Handle receiving posts from other nodes
    # Process the received post and save it to the database
    print("fjdiahflidhflajhsd")
    return Response("123")
