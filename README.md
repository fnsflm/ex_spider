# ex_spider

自用exhentai爬虫脚本，爬取搜索结果以及本子的元数据, 并整理有磁力链接的本子列表

## 脚本环境
- python: 3.12.2
- MongoDB 7.0.7 Community
- pymongo: 4.6.3
- requests: 2.31.0

## 各脚本用途

 - ex_spider_list.py
    - 根据搜索url获取本子列表, 每页的url存在`page_urls.csv`中, 每个本子的url存在`loli_list.csv`中
    - 需修改搜索链接url/cookies/代理proxies, 自行修改工作目录
    - page/number初始是0, 如果程序中途执行失败, 将`page_urls.csv`最后一个序号填到`page`里, 将`loli_list.csv`最后一个序号填在`number`里, 将`page_urls.csv`最后一个url填到`url`里

 - ex_spider_one.py
    - 获取单个本子的元数据, 存到mongodb里
    - 需修改cookies/proxies, 自行修改工作目录
    - 如果程序中断, 修改`start`的值为已爬取本子数, tqdm的总数自行修改(删掉也行)

 - deduplicate.py
    - 数据库根据gid去重

 - add_missing.py
    - 数据库比对`loli_list.csv`找出缺失, 并重新爬取数据

 - get_magnet.py
    - 将数据库中具有磁力链接的本子挑出来, 生成表格`loli_magnet.csv`