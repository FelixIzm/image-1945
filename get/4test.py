from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
#from requests.exceptions import Timeout, HTTPError
import json
import random
import time
import threading
from lxml.html import fromstring
import hashlib
import os
from string import Template
import tempfile
from openpyxl import Workbook
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from io import BytesIO
from zipfile import ZipFile
import csv
import io


image_id=85942988
cookies = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dirpath = tempfile.mkdtemp()
print('dirpath = '+dirpath)

#####################################
def getStringHash(id):
    h = hashlib.md5(str(id).encode()+b'db76xdlrtxcxcghn7yusxjcdxsbtq1hnicnaspohh5tzbtgqjixzc5nmhybeh')
    p = h.hexdigest()
    return str(p)
#####################################
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

def get_lists(image_id):
    getimageinfo_url = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(image_id)
    list_id_images = []
    list_urls_infocards  = []
    res1 = requests.get(info_url)
    print(res1.status_code)
    if(res1.status_code==307):
        cookies = {}
        cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
        cookies['JSESSIONID']=res1.cookies['JSESSIONID']
        cookies['showimage']='0'
        img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
        response = requests.get(img_info)
        response_dict = json.loads(response.text)
        i=0
        for item in response_dict:
            i+=1
            #img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
            list_id_images.append({'id':item['id'],'img':item['img']})
            for id in item['mapData'].keys():
                info_url = 'https://obd-memorial.ru/html/info.htm?id='+str(id)
                list_urls_infocards.append(info_url)
    return(list_id_images,list_urls_infocards, cookies)

#def get_images(list_item_images):
def get_images(item):
    global cookies, zipObj
    #for item in list_item_images:
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(str(item['id']))
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
            print('200')
            location = os.path.abspath(dirpath+"/"+str(item['id'])+'.jpg')
            f = open(location, 'wb')
            f.write(req_img.content)
            f.close()
            name_jpg = str(item['id'])+'.jpg'
            zipObj.writestr(name_jpg, req_img.content)



in_memory = BytesIO()
zipObj = ZipFile(in_memory, "a")

list_images, list_infocards, cookies = get_lists(image_id)
print('img count = ',len(list_images))
print('info count = ',len(list_infocards))
#get_images(list_images, cookies)
#print(list_images)
###################################
with PoolExecutor(max_workers=1) as executor:
   for _ in executor.map(get_images, list_images):
       pass
