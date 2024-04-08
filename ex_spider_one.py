import pymongo
from urllib.parse import urlparse
import requests
import json
import os
from tqdm import tqdm
import time
import random

os.chdir(r'I:\ex_spider')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
table_mongodb= myclient["loli"]['loli_list']
api_url = "https://api.e-hentai.org/api.php"
cookies = {"ipb_member_id": "", "ipb_pass_hash": "", "igneous": ""}
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
start = 19300
loli_list = iter(open('loli_list.csv', 'r', encoding='utf-8').readlines()[start + 1:])
pbar = tqdm(total=19316 - start)
line = True
while line:
    glist =[]
    time.sleep(random.uniform(5, 6))
    for i in range(25):
        line = next(loli_list, 0)
        pbar.update()
        if not line:
            break
        gurl = line.strip().split(',')[-1]
        gurl_parse = urlparse(gurl).path.split('/')
        gallery_id = int(gurl_parse[2])
        gallery_token = gurl_parse[3]
        glist.append([gallery_id, gallery_token])
    post_data = '{"method": "gdata", "gidlist": %s,"namespace": 1}' % json.dumps(glist)
    r = requests.post(api_url, data=post_data, cookies=cookies, headers={'User-Agent': ua, 'Content-Type': 'text/html;charset=UTF-8'}, proxies=proxies)
    lolis = json.loads(r.text)
    table_mongodb.insert_many(lolis['gmetadata'])
pbar.close()