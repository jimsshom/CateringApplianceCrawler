#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import httplib2
import time

global httpConn
httpConn = httplib2.Http(timeout=1)

global startUrl
startUrl = 'http://www.catering-appliance.com/'

def getHtmlContent(url):
    (resp, content) = httpConn.request(url, 'GET')
    return content


def getDetailList():
    fp = open('resut', 'w')

    detailList = []
    categoryList = ['/categories/']
#    categoryList = ['/wheelie-bins/']
    while len(categoryList) > 0:
        print 'cat: %d, item: %d' % (len(categoryList), len(detailList))
        fp.write('cat: %d, item: %d\n' % (len(categoryList), len(detailList)))
        curCat = categoryList.pop()
        url = 'http://www.catering-appliance.com' + curCat
        print 'enter: ' + url
        fp.write('enter: ' + url + '\n')
        html = ''
        try:
            html = getHtmlContent(url)
        except Exception, e:
            print 'query fail: url=%s, e=%s' % (url, e)
            fp.write('query fail: url=%s, e=%s\n' % (url, e))
            time.sleep(1)
            categoryList.append(curCat)
            
        soup = BeautifulSoup(html, 'lxml')
        for panel in soup.select('a[class=panel]'):
            print 'find cat: ' + panel['href']
            fp.write('find cat: ' + panel['href'] + '\n')
            categoryList.append(panel['href'])

        for item in soup.select('#products_wrapper div'):
            if 'pgitem' not in item['class']:
                continue
            for title in item.select('div[class=title]'):
                for a in title.select('a'):
                    print 'find item: ' + a['href']
                    fp.write('find item: ' + a['href'] + '\n')
                    detailList.append(a['href'])
    fp.close()

getDetailList()
