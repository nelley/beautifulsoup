# -*- coding: utf-8 -*-

# Using for remove html tags and
# extract necessary part for mecab

from bs4 import BeautifulSoup
import bs4
import urllib2
import os
import csv
from shutil import copyfile
from datetime import datetime

OUTPUT_FILE_NAME = 'tech_mecab_'


OPEN_PATH = "/home/nelley/casperPractice/Law/tech_job_files/"
#OPEN_PATH = "/home/nelley/beautifulsoup/debug/"
SAVE_PATH = '/home/nelley/beautifulsoup/mecab_' + datetime.now().strftime('%Y%m%d') + '/'


invalid_tags = ['html', 'body', 'head', 'title',  'iframe', 'span', 'div', 'link', 'a', 'meta']
cnt = 1

'''function for remove HTML tags'''
def removeHTML(filename, cnt):
    f = open(SAVE_PATH + OUTPUT_FILE_NAME + '%s.txt' % cnt, "w")
    soup = BeautifulSoup(open(filename), "html.parser")

    # remove all by id
    for div in soup.find_all("div", {'id':'topbar-container'}): 
        div.decompose()

    for div in soup.find_all("div", {'id':'navigation-container'}): 
        div.decompose()
   
    for div in soup.find_all("span", {'class':'push-ipdatetime'}): 
        div.decompose()
 
    # remove all by tag
    [item.extract() for item in soup.contents if isinstance(item, bs4.Doctype)]
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]

    for tag in invalid_tags: 
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    html = "".join(line.strip() for line in str(soup).split("\n"))

    #f.write(str(soup))
    f.write(html)
    f.flush()
    f.close()


''' main process start here!!!'''
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

for content in os.listdir(OPEN_PATH): # "." means current directory
    #print OPEN_PATH + content
    removeHTML(OPEN_PATH + content, cnt)
    cnt += 1

