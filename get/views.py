from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_id =''
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    userform = UserForm({'image_id':image_id})

    return render(request, "get/index.html", {"form": userform,"web_link": "https://drive.google.com"})

# Create your views here.
