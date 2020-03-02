from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import os, tempfile, requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_id =''
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    image_id=0
    userform = UserForm({'image_id':image_id})
    image_id = request.POST.get("image_id")
    url = 'https://www.facebook.com/favicon.ico'
    r = requests.get(url, allow_redirects=True)

    dirpath = tempfile.mkdtemp()

    open(os.path.join(dirpath, 'facebook.ico'), 'wb').write(r.content)
    return render(request, "get/index.html", {"form": userform,"web_link": dirpath})

# Create your views here.
