# -*- encoding: utf-8 -*-

import requests
import json
import os
import re


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def download_skin(skin_js):  # 解析网络js文件
    pattern = re.compile(b'LOLherojs.champion.*=({.*});', re.S)  # 字符为byte类型
    hero = pattern.findall(skin_js)[0]
    # print(hero)
    hero = json.loads(hero)

    for skin in hero['data']['skins']:
        url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big{}.jpg'.format(skin['id'])
        picture = requests.get(url, headers=headers)
        if picture.status_code == 200:
            path = './skins/{}'.format(hero['data']['name']+hero['data']['title'])
            mkdir(path)
            with open(path + '/{}.jpg'.format(skin['name'].split(' ')[0]), 'wb') as f:
                f.write(picture.content)
            print(skin, end='')
            print('下载成功')
        else:
            print(skin, end='')
            print('下载失败')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}

with open('herolist.json', 'r') as f:
    heros = json.load(f)

for hero in heros:
    hero_url = 'http://lol.qq.com/biz/hero/{}.js'.format(hero)
    # print(hero_url)
    skin_js = requests.get(hero_url, headers=headers).content
    # print(skin_js)
    download_skin(skin_js)