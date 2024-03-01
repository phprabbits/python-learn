import requests
import re
import os
import time
import pymysql
import random
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="123456", database="bg", charset='utf8')
cursor = conn.cursor()

url = 'http://www.itokoo.com/read.php?tid=4467'
_html = requests.get(url)
soup = BeautifulSoup(_html.content, 'lxml')
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Referer": "http://www.itokoo.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
}
fileHandle = open('tag.txt', mode='w')
# 生成IP 伪造访问来源，防止IP封禁
ip1 = str(random.randint(100, 249))
ip2 = str(random.randint(100, 249))
ip3 = str(random.randint(100, 249))
ip4 = str(random.randint(100, 249))

mimSql = 'SELECT min(from_id) as min FROM bg where type = 20'
cursor.execute(mimSql)
# # 获取所有记录列表
minRow = cursor.fetchone()

if minRow[0] :
    mid = int(minRow[0])
else :
    mid = 9999999

print(mid)
proxies = {'http://': 'http:' + ip1 + '.' + ip2 + '.' + ip3 + '.' + ip4}
html = requests.get(url, headers=headers, proxies=proxies, timeout=5)
if html.status_code == 200:
    soup = BeautifulSoup(html.content, 'lxml')
    aBoxList = soup.select('.tpc_content a')
    print(len(aBoxList))
    list = {}
    hrefList = []
    numList = []

    # 抓取单个页面
    for li, lv in enumerate(aBoxList):
        # 将当前的ID插入post表
        id = int(re.findall(r'\d+', lv.attrs['href'])[0])
        print(id)
        if id < mid :
            # id = 35113
            sql = 'SELECT id FROM bg WHERE from_id = ' + str(id)
            cursor.execute(sql)
            # 获取所有记录列表
            result = cursor.fetchone()
            result = []
            if not result :
                title = lv.get_text()
                src = 'http://www.itokoo.com/read.php?tid=' + str(id)
                print(id)
                # src = 'http://www.itokoo.com/read.php?tid=37656'
                res = requests.get(src, headers=headers, proxies=proxies, timeout=200)
                soupRes = BeautifulSoup(res.content, 'lxml')
                boxContent = soupRes.select('#read_tpc')
                if len(boxContent) > 0 :
                    boxList = soupRes.select('#read_tpc')[0]
                    baidu = boxList.select('.down')
                    if len(baidu) > 0:
                        baiduUrl = baidu[-1].attrs['href']
                        content = boxList.select('font')[0]
                        content = content.get_text('<br>')
                        string = content.split('<br>')
                        # 模特
                        model = string[0].split(' ')[-1]
                        # 尺寸
                        size = string[1].split(':')[-1].split('×')
                        width = int(re.findall(r'\d+', size[0])[0])
                        height = int(re.findall(r'\d+', size[1])[0])
                        # info
                        info = string[2].split(':')[-1]
                        print(info.find('/'))
                        if info.find('/') > 0 :
                            # 数量
                            infoSplit = string[2].split(':')[-1].split('/')
                            num = int(re.findall(r'\d+', infoSplit[0])[0])
                            # 图片占用空间
                            space = re.findall(r'\d+', infoSplit[1])
                            mem = 0
                            if len(space) > 0:
                                mem = int(space[0])
                        else :
                            num = 0
                            mem = 0
                        # 获取提取码
                        codeHtml = baidu[-1]
                        code = boxList.get_text('').split(': ')[-1]
                        # 插入数据库
                        postSql = 'insert into bg(type,from_id,title,bdy_link,bdy_pass,model,width,height,num,mem,create_time,update_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        insertData = [20, id, title, baiduUrl, code, model, width, height, num, mem, int(time.time()), int(time.time())]
                        cursor.execute(postSql, insertData)
                        conn.commit()
                        postId = cursor.lastrowid  # 获取新增数据自增ID

                    time.sleep(0.2)
            else :
                title = lv.get_text()
                src = 'http://www.itokoo.com/read.php?tid=' + str(id)
                print(id)
                # src = 'http://www.itokoo.com/read.php?tid=37656'
                res = requests.get(src, headers=headers, proxies=proxies, timeout=200)
                soupRes = BeautifulSoup(res.content, 'lxml')
                boxContent = soupRes.select('#read_tpc')
                if len(boxContent) > 0 :
                    boxList = soupRes.select('#read_tpc')[0]
                    baidu = boxList.select('.down')
                    if len(baidu) > 0:
                        baiduUrl = baidu[-1].attrs['href']
                        content = boxList.select('font')[0]
                        content = content.get_text('<br>')
                        string = content.split('<br>')
                        # 模特
                        model = string[0].split(' ')[-1]
                        # 尺寸
                        size = string[1].split(':')[-1].split('×')
                        width = int(re.findall(r'\d+', size[0])[0])
                        height = int(re.findall(r'\d+', size[1])[0])
                        # info
                        info = string[2].split(':')[-1]
                        print(info.find('+1'))
                        if info.find('+1') :
                            # 数量
                            infoSplit = string[2].split(':')[-1].split('+1')
                            num = int(re.findall(r'\d+', infoSplit[0])[0])
                            # 图片占用空间
                            space = re.findall(r'\d+', infoSplit[1])
                            mem = 0
                            if len(space) > 0:
                                mem = int(space[0])
                        else :
                            num = 0
                            mem = 0
                        # 获取提取码
                        codeHtml = baidu[-1]
                        code = boxList.get_text('').split(': ')[-1]
                        print(title, baiduUrl, code, model, width, height, num, mem)
                        # 插入数据库
                        postSql = 'update bg set bdy_pass = %s where from_id = "%s" '
                        cursor.execute(postSql, [code, id])
                        conn.commit()
                        postId = cursor.lastrowid  # 获取新增数据自增ID

                    time.sleep(0.2)
time.sleep(2)

