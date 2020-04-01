#from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import requests
#from requests.exceptions import Timeout, HTTPError
import json
import random
import time
from lxml.html import fromstring
import hashlib
import os
from string import Template
import tempfile
from openpyxl import Workbook
from io import BytesIO
from zipfile import ZipFile
import csv
import io
import aiohttp
import asyncio


image_id = 85942988 # 6
#image_id = 70782617 #482
cookies = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#dirpath = tempfile.mkdtemp()
#print('dirpath = '+dirpath)
in_memory = BytesIO()
zipObj = ZipFile(in_memory, "a")
global_i = 0
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

headers_img = parse_file(BASE_DIR+'/header_img.txt')
headers_302 = parse_file(BASE_DIR+'/header_302.txt')

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
        for item in response_dict:
            #img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
            list_urls_infocards  = []
            for id in item['mapData'].keys():
                list_urls_infocards.append('https://obd-memorial.ru/html/info.htm?id='+str(id))
            list_id_images.append({'id':item['id'],'img':item['img'],'urls_infocards':list_urls_infocards})
    return(list_id_images, cookies)

#def get_images(list_item_images):
def get_images(item):
    global cookies, zipObj
    global header_img, headers_302
    #for item in list_item_images:
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(str(item['id']))
    img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
    headers_302['Cookie'] = make_str_cookie(cookies)
    headers_302['Referer'] = info_url
    req302 = requests.get(img_url,headers=headers_302,cookies=cookies, allow_redirects = False)
    if(req302.status_code==302):
        params = {}
        params['id'] = str(item['id'])
        params['id1'] = getStringHash(item['id'])
        params['path'] = item['img']
        headers_img['Referer'] = info_url
        #####################
        req_img = requests.get("https://cdn.obd-memorial.ru/html/images3", headers=headers_img, params=params, cookies=cookies, stream=True, allow_redirects=False )
        #####################
        if(req_img.status_code==200):
            name_jpg = str(item['id'])+'.jpg'
            zipObj.writestr(name_jpg, req_img.content)

async def get_images_async(item, cookies, header_img):
    global headers_302, global_i
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(str(item['id']))
    img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
    params = {}
    params['id'] = str(item['id'])
    params['id1'] = getStringHash(item['id'])
    params['path'] = item['img']

    headers_302 = parse_file(BASE_DIR+'/header_302.txt')
    headers_302['Cookie'] = make_str_cookie(cookies)
    headers_302['Referer'] = info_url
    async with aiohttp.ClientSession() as session:
        async with session.get("https://obd-memorial.ru/html/images3",params=params,headers=headers_302,cookies=cookies) as resp:
            #while not resp.content.at_eof():
            #    line = await resp.content.read()
            
            #print(global_i,item['id'])
            return await resp.content.read(), item['id']
            #print(await resp.text())


'''
    req302 = requests.get(img_url,headers=headers_302,cookies=cookies, allow_redirects = False)
    if(req302.status_code==302):
        params = {}
        params['id'] = str(item['id'])
        params['id1'] = getStringHash(item['id'])
        params['path'] = item['img']
        headers_img['Referer'] = info_url
        #####################
        req_img = requests.get("https://cdn.obd-memorial.ru/html/images3", headers=headers_img, params=params, cookies=cookies, stream=True, allow_redirects=False )
        #####################
        if(req_img.status_code==200):
            name_jpg = str(item['id'])+'.jpg'
            zipObj.writestr(name_jpg, req_img.content)
'''

async def get(url, cookies, headers):
    headers['Referer'] = 'https://obd-memorial.ru/html/info.htm?id='.format(id)
    #url = 'https://obd-memorial.ru/html/info.htm?id='.format(id)
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.get(url) as resp:
            return resp
######################################



list_images, cookies = get_lists(image_id)
#print('img count = ', list_images)
#print('cookies = ',cookies)
in_memory = BytesIO()
zipObj = ZipFile(in_memory, "a")

loop = asyncio.get_event_loop()
coroutines = [get_images_async(item, cookies, headers_img) for item in list_images]
results = loop.run_until_complete(asyncio.gather(*coroutines))
print(len(results))
for res in results:
    #print(res[0])
    name_jpg = str(res[1])+'.jpg'
    zipObj.writestr(name_jpg, res[0])

in_memory.seek(0)    

with open("my_zip.zip", "wb") as f: # use `wb` mode
    f.write(in_memory.read())

exit(1)
#get_images(list_images, cookies)
#print(list_images)
###################################

headers_img = parse_file(BASE_DIR+'/header_img.txt')
headers_img['cookies'] = make_str_cookie(cookies)
headers_img['Referer'] = 'https://obd-memorial.ru/html/info.htm?id={}'.format(image_id)






for file in zipObj.filelist:
    file.create_system = 0

zipObj.close()
in_memory.seek(0)    
print(zipObj.filelist)

with open('test.zip', 'wb') as f:
    f.write(in_memory.read())
