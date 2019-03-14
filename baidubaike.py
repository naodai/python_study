# -*- coding: utf-8 -*-
import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host='127.0.0.1', user='root', passwd="Root", db='univ', charset='utf8')
cur = conn.cursor()

BAIKE_URL = 'https://baike.baidu.com/item/'

HEADER = {
    'Host': 'baike.baidu.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
}

SQL_BASE = "select id,name from gaokao_univ_one order by id asc limit "

start = 0
run = 1
while run:
    sql = SQL_BASE + str(start) + ',1'
    # try:
    cur.execute(sql)
    result = cur.fetchone()
    if (result):
        print(result[0])
        print(result[1])
        url = BAIKE_URL + result[1]
        print(url)

        request = requests.get(url, headers=HEADER, allow_redirects=False)
        request.encoding = 'utf-8'
        # print(request.status_code)
        # print(request.headers)
        # print(request.encoding)
        # print(request.text)
        soup = BeautifulSoup(request.text, 'lxml')
        basicInfo_item = soup.select('.basicInfo-item')
        # print(basicInfo_item[0].text)
        i = 0
        univ_jiancheng = ''
        univ_yingwenming = ''
        univ_chuangbanshijian = ''
        univ_liebie = ''
        univ_daima = ''
        univ_dizhi = ''
        univ_bumen = ''
        univ_diqu = ''

        for one in basicInfo_item:
            # print(one.text.strip())
            if (one.text.strip() == '中文名'):
                print('中文名' + basicInfo_item[i + 1].text)
            elif (one.text.strip() == '英文名' or one.text.strip() == '外文名'):
                # print('英文名' + basicInfo_item[i + 1].text)
                univ_yingwenming = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '简    称'):
                # print('简    称' + basicInfo_item[i + 1].text)
                univ_jiancheng = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '创办时间'):
                # print('创办时间' + basicInfo_item[i + 1].text)
                univ_chuangbanshijian = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '类    别'):
                # print('类    别' + basicInfo_item[i + 1].text)
                univ_liebie = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '学校代码'):
                # print('学校代码' + basicInfo_item[i + 1].text)
                univ_daima = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '学校地址' or one.text.strip() == '地    址'):
                # print('学校地址' + basicInfo_item[i + 1].text)
                univ_dizhi = basicInfo_item[i + 1].text.strip()
                if (len(univ_dizhi) > 240):
                    univ_dizhi = univ_dizhi[0:250]
                univ_dizhi = pymysql.escape_string(univ_dizhi)
            elif (one.text.strip() == '主管部门'):
                # print('主管部门' + basicInfo_item[i + 1].text)
                univ_bumen = pymysql.escape_string(basicInfo_item[i + 1].text.strip())
            elif (one.text.strip() == '所属地区'):
                # print('所属地区' + basicInfo_item[i + 1].text)
                univ_diqu = pymysql.escape_string(basicInfo_item[i + 1].text.strip())

            i = i + 1
        update_sql = "update gaokao_univ_one set english_name='" + univ_yingwenming + "',jiancheng='" + univ_jiancheng + "',createtime='" + univ_chuangbanshijian + "',leibie='" + univ_liebie + "',address='" + univ_dizhi + "',diqu='" + univ_diqu + "',code='" + univ_daima + "',zhuguan='" + univ_bumen + "' where id =" + \
                     str(result[0])
        print(update_sql)
        cur.execute(update_sql)
        conn.commit()
        start = start + 1
        if (start > 2651):
            print('OK')
            run = 0
    else:
        print('none')
        run = 0
    # except:
    #     print(sql)
    #     start = start + 1

conn.close()
