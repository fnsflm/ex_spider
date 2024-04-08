import pymongo
import numpy as np

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
table_mongodb= myclient["loli"]['loli_list']
gid_dic_list = table_mongodb.find({}, {'_id':0, 'gid':1})
gid_list = [i['gid'] for i in gid_dic_list]
gids, gid_counts = np.unique(gid_list, return_counts=True)
gid_duplicate = gids[gid_counts > 1]
# 取出一个, 其他全删
for gid in gid_duplicate:
    duplicates = list(table_mongodb.find({'gid': int(gid_duplicate[0])}))
    reserve = duplicates[0]
    delete_ids = [i['_id'] for i in duplicates]
    table_mongodb.delete_many({'_id': {'$in': delete_ids}})
    table_mongodb.insert_one(reserve)