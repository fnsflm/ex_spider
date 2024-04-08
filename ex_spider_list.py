import requests
import random
from bs4 import BeautifulSoup
import time
import os

number = 18900 # 0
page = 756  # 0
url = "https://exhentai.org/?f_search=f:lolicon%24+l:chinese%24+&next=262764" # page+1的url

os.chdir(r'I:\ex_spider')
cookies = {"ipb_member_id": "", "ipb_pass_hash": "", "igneous": ""}
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
result_csv = open('loli_list.csv', 'a', encoding='utf-8')
page_csv = open('page_urls.csv', 'a', encoding='utf-8')
if number == 0:
    result_csv.write('number,page,name,url\n')
    page_csv.write('page,url\n')



def random_interval(start=1, end=2):
    time.sleep(random.uniform(start, end))

def get_one_page(bs):
    global number, page
    table_trs = bs.find('table', class_='gltc').find_all('tr')[1:]
    for tr in table_trs:
        number += 1
        a = tr.find('td', class_="glname").find('a')
        url_one = a.attrs['href']
        name = a.find('div', class_='glink').text
        result_csv.write(f'{number},{page},"{name}",{url_one}\n')
        result_csv.flush()
        print(number, name)
    next_a = bs.find('a', id='unext')
    if not next_a:
        return
    next_url = next_a.attrs['href']
    return next_url
    

def main():
    global page
    next_url = url
    while next_url:
        random_interval()
        page += 1
        page_csv.write(f'{page},{next_url}\n')
        page_csv.flush()
        tries = 5
        while tries:
            try:
                r = requests.get(next_url, headers={'User-Agent': ua, 'Content-Type': 'text/html;charset=UTF-8'}, cookies=cookies, proxies=proxies)
                break
            except Exception as e:
                print(e)
                time.sleep(10)
                tries -= 1

        r.encoding='utf-8'
        bs = BeautifulSoup(r.text, 'html.parser')
        next_url = get_one_page(bs)

if __name__ == '__main__':
    main()
    
