from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import os, tempfile, requests, time
import get_image_google

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_id =''
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    image_id=0
    userform = UserForm({'image_id':image_id})
    image_id = request.POST.get("image_id")
    url = 'https://www.facebook.com/favicon.ico'
    r = requests.get(url, allow_redirects=True)


    image_id = 51480906
    link = ''
    d = {'image':True, 'excel':False}
    if __name__ == "__main__":
        link = get_image_google.main(image_id,**d)
        #link = get_image_google.save_to_folder(str(image_id),list_file)
        # отладка
        #link = get_image_google.mmm()

        #open(os.path.join(dirpath, 'facebook.ico'), 'wb').write(r.content)
    return render(request, "get/index.html", {"form": userform,"web_link": link})

# Create your views here.
