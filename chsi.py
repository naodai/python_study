#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host='127.0.0.1', user='root', passwd="Root", db='univ')
cur = conn.cursor()

chsi_domain = 'https://gaokao.chsi.com.cn'
chsi_url = chsi_domain + '/sch/search.do'

offset = 0
run = 1
while run:
    url = chsi_url + '?start=' + str(offset)
    print(url)
    chsi_body = requests.get(url)
    soup = BeautifulSoup(chsi_body.text, 'lxml')

    univ_tr = soup.select('.ch-table tr')
    for tr in univ_tr:
        td = tr.find_all('td')
        td_i = 0
        univ_name = ''
        univ_link = ''
        univ_city = ''
        univ_lishu = ''
        univ_type = ''
        univ_xueli_cengci = ''
        univ_yuanxiaotexing = ''
        univ_985 = ''
        univ_211 = ''
        univ_yanjiusheng = ''
        for item in td:
            if td_i == 0:
                univ_name = item.text.strip()
                a = item.find('a')
                if a:
                    univ_link = chsi_domain + item.a['href']
            elif td_i == 1:
                univ_city = item.text.strip()
            elif td_i == 2:
                univ_lishu = item.text.strip()
            elif td_i == 3:
                univ_type = item.text.strip()
            elif td_i == 4:
                univ_xueli_cengci = item.text.strip()
            elif td_i == 5:
                span = item.find_all('span')
                for spanText in span:
                    texing = spanText.text.strip()
                    if(texing == '985'):
                        univ_985 = '1'
                    elif(texing == '211'):
                        univ_211 = '1'
            elif td_i == 6:
                univ_yanjiusheng = item.text.strip()
                if univ_yanjiusheng != '':
                    univ_yanjiusheng = '1'
                else:
                    univ_yanjiusheng = '0'
            td_i = td_i + 1
        # 写入数据库
        if univ_name:
            sql = "insert into univ "
            sql = sql + "(name,link,province,lishu,leixing,xuelicengci,yuanxiaotexing_985,yuanxiaotexing_211,yanjiushengyuan) "
            sql = sql + " values "
            sql = sql + "('"+ univ_name + "','" + univ_link + "','" + univ_city + "','" + univ_lishu + "','" + univ_type + "','" + univ_xueli_cengci + "','" + univ_985 + "','" + univ_211 + "','" + univ_yanjiusheng + "')"
            cur.execute(sql)
            conn.commit()
    if offset > 2720:
        run = 0
        break
    offset = offset + 20

cur.close()
conn.close()
print('ok')
