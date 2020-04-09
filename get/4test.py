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
import async_timeout


image_id = 85942988 # 6
#image_id = 70782617 #482
#image_id = 3878518 #21
#image_id = 6937337 # 66
#image_id = 
#image_id =  
cookies = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        try:
            cookies['3fbe47cd30daea60fc16041479413da2']=res1.cookies['3fbe47cd30daea60fc16041479413da2']
            cookies['JSESSIONID']=res1.cookies['JSESSIONID']
        except KeyError:
            print("KeyError")
            exit(1)

        cookies['showimage']='0'
        img_info = 'https://obd-memorial.ru/html/getimageinfo?id={}'.format(image_id)
        print(img_info)
        response = requests.get(img_info)
        try:
            response_dict = json.loads(response.text)
        except JSONDecodeError:
            print("JSONDecodeError")
            exit(1)
        print(len(response_dict))
        for item in response_dict:
            #img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
            list_urls_infocards  = []
            for id in item['mapData'].keys():
                list_urls_infocards.append('https://obd-memorial.ru/html/info.htm?id='+str(id))
            list_id_images.append({'id':item['id'],'img':item['img'],'urls_infocards':list_urls_infocards})
    return(list_id_images, cookies)


async def get_images_async(session,item, cookies, header_img):
    global headers_302
    info_url = 'https://obd-memorial.ru/html/info.htm?id={}'.format(str(item['id']))
    img_url="https://obd-memorial.ru/html/images3?id="+str(item['id'])+"&id1="+(getStringHash(item['id']))+"&path="+item['img']
    params = {}
    params['id'] = str(item['id'])
    params['id1'] = getStringHash(item['id'])
    params['path'] = item['img']

    headers_302['Cookie'] = make_str_cookie(cookies)
    headers_302['Referer'] = info_url
    #with aiohttp.ClientSession() as session:
    data = bytearray()
    buffer = b""
    async with session.get("https://obd-memorial.ru/html/images3",params=params,headers=headers_302,cookies=cookies, read_until_eof=True) as resp:
        #print(item['id'])
        #assert resp.status == 200
        #return await resp.content.readany(), item['id']
        '''
        async for data, end_of_http_chunk in resp.content.iter_chunks():
            buffer += data
            print(item['id'], len(data))
            if end_of_http_chunk:
                print(len(buffer))
                return buffer, item['id']
'''

        while True:
            chunk = await resp.content.read()
            if not chunk:
                break
            data += chunk
    return data, item['id']

    

async def main():            
    list_images, cookies = get_lists(image_id)
    #in_memory = BytesIO()
    #zipObj = ZipFile(in_memory, "a")

    print('1')
    loop = asyncio.get_running_loop()
    print('2')
    async with aiohttp.ClientSession(loop=loop) as session:
        print('3')
        coroutines = [get_images_async(session,item, cookies, headers_img) for item in list_images]
        #results = loop.run_until_complete(asyncio.gather(*coroutines))
        return await asyncio.gather(*coroutines)

r = asyncio.run(main())
print('===================')
for item in r:
    name_jpg = str(item[1])+'.jpg'
    zipObj.writestr(name_jpg, item[0])
    print(len(item[0]),item[1])

for file in zipObj.filelist:
    file.create_system = 0
zipObj.close()
in_memory.seek(0)    

with open('1.zip', 'wb') as f:
    f.write(in_memory.read())

exit(1)

