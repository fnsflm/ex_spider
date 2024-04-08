import pymongo
from urllib.parse import urlparse
import requests
import json
import os
import time
import random

os.chdir(r'I:\ex_spider')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
table_mongodb= myclient["loli"]['loli_list']
api_url = "https://api.e-hentai.org/api.php"
cookies = {"ipb_member_id": "", "ipb_pass_hash": "", "igneous": ""}
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}

def get_missing_list():
    now_gid_ls = table_mongodb.find({}, {'_id': 0, 'gid': 1})
    now_set = [i['gid'] for i in now_gid_ls]
    loli_list = open('loli_list.csv', 'r', encoding='utf-8').readlines()
    should_set = [int(urlparse(i.split(',')[-1]).path.split('/')[2]) for i in loli_list[1:]]
    missing_gids = list(set(should_set) - set(now_set))
    missing_ids = [should_set.index(gid) for gid in missing_gids]
    return [loli_list[i + 1] for i in missing_ids]

loli_list = iter(get_missing_list())
line = True
while line:
    glist =[]
    time.sleep(random.uniform(5, 6))
    for i in range(25):
        line = next(loli_list, 0)
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