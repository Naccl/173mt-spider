#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Naccl
# python3 main.py https://173mt.com/cn/39531.html

import requests
from bs4 import BeautifulSoup
import os
import sys


dirPathPrefix = "./"


def httpGet(url):
    print(url)
    try:
        response = requests.get(url, timeout=(3, 3))
        if response.status_code == 200:
            return response
    except Exception as e:
        print(e)
        for i in range(1,4):
            print("Retry: %s, url: %s" % (i, url))
            response = requests.get(url, timeout=(3, 3))
            if response.status_code == 200:
                return response
    return -1


def mkdirs(bs):
    title = bs.title.string.rsplit("-", 1)[0][:-1]
    print(title)
    dirPath = dirPathPrefix + title + "/"
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    return dirPath


def getBeautifulSoup(url):
    r = httpGet(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, "lxml")


def getPageNum(bs):
    pageButtonList = bs.select("body > section > div.article-paging > a > span")
    return len(pageButtonList)


def getImgSrcList(bs, imgSrcList):
    img = bs.select("body > section > article > p > a > img")
    for i in img:
        imgSrcList.append(i['data-src'])


def saveImg(imgSrcList, dirPath):
    imgCnt = 1
    for i in imgSrcList:
        r = httpGet(i)
        with open(dirPath + str(imgCnt) + "." + i.rsplit(".", 1)[1], "wb") as f:
            f.write(r.content)
        imgCnt += 1


def main(url):
    bs = getBeautifulSoup(url)
    dirPath = mkdirs(bs)
    pageNum = getPageNum(bs)
    imgSrcList = []
    getImgSrcList(bs, imgSrcList)
    for p in range(2, pageNum + 2):
        nextUrl = url[:-5] + "_" + str(p) + ".html"
        bs = getBeautifulSoup(nextUrl)
        getImgSrcList(bs, imgSrcList)
    saveImg(imgSrcList, dirPath)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        main(args[1])
    else:
        print("Input a url of the first page")
