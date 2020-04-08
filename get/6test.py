from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.utils.encoding import smart_str

from .forms import FormSelectId
import os

import requests, json
import hashlib
import lxml.html as html

from string import Template
import tempfile
from openpyxl import Workbook
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import csv
import io

image_id = ''
##########################################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cols = ['ID scan','ID','Фамилия','Имя','Отчество','Дата рождения/Возраст','Место рождения','Дата и место призыва','Последнее место службы','Воинское звание','Судьба','Дата смерти','Первичное место захоронения']

######################################
def parse_file (name_file):
    dict_ = {}
    f = open(name_file, 'r')
    s = f.read()
    dict_={}
    list_ = s.splitlines()
    for item in list_:
        items = item.split(":")
        dict_[items[0]] = items[1].lstrip()
    return dict_
#####################################
def make_str_cookie(cookies):
    str_cook = ''
    for key, value in cookies.items():
        str_cook += '{0}={1};'.format(key,value)
    return str_cook
#####################################
def getStringHash(id):
    h = hashlib.md5(str(id).encode()+b'db76xdlrtxcxcghn7yusxjcdxsbtq1hnicnaspohh5tzbtgqjixzc5nmhybeh')
    p = h.hexdigest()
    return str(p)
#####################################
def get_info(id_scan,id,cookies):
    cookies['showimage']='0'
    info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
    res3 = requests.get(info_url,cookies=cookies)
    doc = html.fromstring(res3.text)
    divs = {}
    for div in doc.find_class('card_parameter'):
        divs[div.getchildren()[0].text_content()] = div.getchildren()[1].text_content()
        #print ('%s: %s' % (div.getchildren()[0].text_content(), div.getchildren()[1].text_content()))
    list_col = []
    for col in cols:
        if(col in divs.keys()):
            list_col.append(divs[col])
        else:
            list_col.append('')
    list_col[1] = id
    list_col[0] = id_scan
    return list_col

#####################################
#            MAIN!!!!!!!!!!         #
#####################################
def local_main(image_id):
    if(image_id == None):
        return 'Ссылка на каталог -', ''
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(image_id)
    img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
    res1 = requests.get(info_url, allow_redirects = True)

    in_memory = BytesIO()
    zipObj = ZipFile(in_memory, "a")

    if(res1.status_code==307):
        if(not '3fbe47cd30daea60fc16041479413da2' in res1.cookies):
            return 'no folder','Запись сводного документа не найдена' 
        cookies = {}
        cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
        cookies['JSESSIONID']=res1.cookies['JSESSIONID']
        #############################
        #   load list id's images   #
        #############################
        response = requests.get(img_info,cookies=cookies)
        response_dict = json.loads(response.text)
        print('response_dict = '+str(len(response_dict)))
        #############################
        #if(excel):
        columns = cols
        row_csv = []
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        for col_num, column_title in enumerate(cols, 1):
            row_csv.append(column_title)
        writer.writerow(row_csv)
        # идем по списку id сканов
        for item in response_dict:
            #if(excel):
            for id in item['mapData'].keys():
                row = get_info(item['id'],id,cookies)
                row_csv = []
                for col_num, cell_value in enumerate(row, 1):
                    row_csv.append(cell_value)
                writer.writerow(row_csv)
            #if(image):
            img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
            headers_302 = parse_file(BASE_DIR+'/header_302.txt')
            headers_302['Cookie'] = make_str_cookie(cookies)
            headers_302['Referer'] = info_url
            req302 = requests.get(img_url,headers=headers_302,cookies=cookies, allow_redirects = False)
            if(req302.status_code==302):
                params = {}
                params['id'] = str(item['id'])
                params['id1'] = getStringHash(item['id'])
                params['path'] = item['img']
                headers_img = parse_file(BASE_DIR+'/header_img.txt')
                headers_img['Referer'] = info_url
                #####################
                req_img = requests.get("https://cdn.obd-memorial.ru/html/images3",headers=headers_img,params=params,cookies=cookies,stream = True,allow_redirects = False )
                #####################
                if(req_img.status_code==200):
                    name_jpg = str(item['id'])+'.jpg'
                    zipObj.writestr(name_jpg, req_img.content)

        zipObj.writestr(str(image_id)+'_book.csv', output.getvalue())
        # fix for Linux zip files read in Windows
        for file in zipObj.filelist:
            file.create_system = 0
    zipObj.close()
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename="+str(image_id)+".zip"
    in_memory.seek(0)    
    response.write(in_memory.read())
    return response

#####################################################
def index(request):
    print(" __name__ = "+str(__name__))
    link = ''
    _id = '0'
    form_dir = FormSelectId({'_id':_id})
    if("SelectId" in request.POST):
        image_id = request.POST.get("_id")
        if(image_id == '0'):
            return render(request, "get/index.html", {"form_dir": form_dir })
        #image_id = 85942988
        return local_main(image_id)

    else:
        return render(request, "get/index.html", {'form_dir':form_dir})

# Create your views here.

