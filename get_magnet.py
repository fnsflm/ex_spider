import pymongo
import pandas as pd
import os
import time

os.chdir(r'I:\ex_spider')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
table_mongodb= myclient["loli"]['loli_list']
loli_torrents_csv = open('loli_torrents.csv', 'w', encoding='utf-8')
loli_torrents_csv.write('name,time,rate,page,url,magnet\n')

def select_one(torrents):
    if len(torrents) == 1:
        return torrents[0]['hash']
    else:
        df = pd.DataFrame(torrents)
        return df.hash[df.fsize.idxmax()]

magnet_hash_dic = table_mongodb.find({'torrents': {'$exists': True, '$ne': []}}, )
for i in magnet_hash_dic:
    hash = select_one(i['torrents'])
    name = i['title_jpn']
    if not name:
        name = i['title']
    url = f'https://exhentai.org/g/{i['gid']}/{i['token']}'
    page = i['filecount']
    rate = i['rating']
    magnet = f'magnet:?xt=urn:btih:{hash}'
    time_stamp = i['posted']
    timeArray = time.localtime(int(time_stamp))
    otherStyleTime = time.strftime(r"%Y-%m-%d %H:%M:%S", timeArray)
    loli_torrents_csv.write(f'"{name}","{otherStyleTime}",{rate},{page},{url},{magnet}\n')