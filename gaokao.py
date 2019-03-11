#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import time

import pymysql
import requests
from bs4 import BeautifulSoup

IMAGE_PATH = './gaokao/avatar/'


def create_path(file_path):
    # 是否有这个路径
    if not os.path.exists(file_path):
        # 创建路径
        os.makedirs(file_path)


def urllib_download(image_url, name):
    from urllib.request import urlretrieve
    try:
        filename = name + '.png'
        urlretrieve(image_url, IMAGE_PATH + filename)
        return filename
    except IOError as e:
        return ''
    except Exception as e:
        return ''


create_path(IMAGE_PATH)

conn = pymysql.connect(host='127.0.0.1', user='root', passwd="Root", db='univ')
cur = conn.cursor()

gaokao_domain = 'http://college.gaokao.com'
gaokao_url_path = '/schlist/p'

page = 1
run = 1
while run:
    url = gaokao_domain + gaokao_url_path + str(page) + '/'
    print(url)
    gaokao_body = requests.get(url)
    soup = BeautifulSoup(gaokao_body.text, 'lxml')
    dl = soup.select('div.scores_List dl')

    for item in dl:
        univ_name = ''
        univ_img_url = ''
        univ_img_save = ''
        univ_gaokao_link = ''
        univ_di = ''
        univ_985 = ''
        univ_211 = ''
        univ_leixing = ''
        univ_lishu = ''
        univ_xingzhi = ''
        univ_wangzhi = ''

        img = item.find('img')
        a = img.find_parent('a')
        if (a):
            univ_gaokao_link = a['href']
        univ_img_url = img['src']
        univ_name = img['alt']
        print(univ_name)
        univ_img_save = urllib_download(univ_img_url, univ_name)

        li = item.find_all('li')
        li_i = 0
        for li_item in li:
            if (li_i == 0):
                univ_di = li_item.text.replace('高校所在地：', '').strip()
            elif (li_i == 1):
                tese = li_item.text.strip()
                if (tese.find('985') > -1):
                    univ_985 = '1'
                else:
                    univ_985 = '0'
                if (tese.find('211') > -1):
                    univ_211 = '1'
                else:
                    univ_211 = '0'
            elif (li_i == 2):
                univ_leixing = li_item.text.replace('高校类型：', '').strip()
            elif (li_i == 3):
                univ_lishu = li_item.text.replace('高校隶属：', '').strip()
            elif (li_i == 4):
                univ_xingzhi = li_item.text.replace('高校性质：', '').strip()
            elif (li_i == 5):
                univ_wangzhi = li_item.text.replace('学校网址：', '').strip()

            li_i = li_i + 1
        # 写入数据库
        if univ_name:
            sql = "insert into gaokao_univ "
            sql = sql + "(name,logo_url,logo_save,priv,`985`,`211`,type,dependent,property,web,gaokao_link) "
            sql = sql + " values "
            sql = sql + "('" + univ_name + "','" + univ_img_url + "','" + univ_img_save + "','" + univ_di + "','" + univ_985 + "','" + univ_211 + "','" + univ_leixing + "','" + univ_lishu + "','" + univ_xingzhi + "','" + univ_wangzhi + "','" + univ_gaokao_link + "')"
            cur.execute(sql)
            conn.commit()

    time.sleep(2)
    page = page + 1
    if (page > 107):
        run = 0
        break
cur.close()
conn.close()
print('ok')
