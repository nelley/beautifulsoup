# -*- coding: utf-8 -*-

# Using for remove html tags and
# create csv file that in order to import into XAMINER

from bs4 import BeautifulSoup
import bs4
import urllib2
import os
import csv
from shutil import copyfile
from datetime import datetime

POSTER_ptt = u'作者'
CREATETIME_ptt = u'時間'
TITLE_ptt = u'標題'

DOCLINK = 'native/'
TEXTLINK = 'text/'
OUTPUT_FILE_NAME = 'tech_pure_'

CSV_TITLE = [["LIV.Doc ID", "APP.Last saved by", "APP.Title", "FS.Last Modified Date", "APP.Category", "DOCLINK", "TEXTLINK"]]

#OPEN_PATH = "/home/nelley/casperPractice/Law/tech_job_files/"
OPEN_PATH = "/home/nelley/beautifulsoup/debug/"
SAVE_PATH = '/home/nelley/beautifulsoup/xaminer_import_' + datetime.now().strftime('%Y%m%d') + '/'

invalid_tags = ['html', 'body', 'head', 'title',  'iframe', 'span', 'div', 'link', 'a', 'meta']
cnt = 1


'''function for create loadfile.txt'''
def generateCSV(f, s, originFname):
    if not os.path.isfile(SAVE_PATH + 'loadfile.txt'):
        #print SAVE_PATH + 'loadfile.txt'
        #print 'file does not exist'
        with open(SAVE_PATH + 'loadfile.txt', 'w') as fp:
            a = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_ALL)
            a.writerows(CSV_TITLE)
            fp.close()

    #append data into array
    csv_content = []
    csv_content.append(["", "no poster", "no title", "1985/4/5 15:29:05", "no category", "no native" ,"no text"])
    #append filename to txt
    csv_content[0][0] = f

    #append id, title, time
    for i in s.findAll('div', {"class", "article-metaline"}):
        for k in i.findAll('span', {"class":"article-meta-tag"}):
            if (''.join(k.findAll(text=True)).encode('utf8') == POSTER_ptt.encode('utf8')):
                #print 'POSTER'
                for k in i.findAll('span', {"class":"article-meta-value"}):
                    csv_content[0][1] = ''.join(k.findAll(text=True)).encode('utf8')
            elif(''.join(k.findAll(text=True)).encode('utf8') == CREATETIME_ptt.encode('utf8')):
                #print 'time'
                for k in i.findAll('span', {"class":"article-meta-value"}):
                    try:
                        date_object = datetime.strptime(''.join(k.findAll(text=True)), '%a %b %d %H:%M:%S %Y')
                        #print date_object.strftime('%Y/%m/%d %H:%M:%S')
                        csv_content[0][3] = date_object.strftime('%Y/%m/%d %H:%M:%S')
                    except ValueError:
                        #print 'ValueError happened' + originFname
                        csv_content[0][3] = '1985/4/5 15:29:05'

            elif(''.join(k.findAll(text=True)).encode('utf8') == TITLE_ptt.encode('utf8')):
                #print 'title'
                for k in i.findAll('span', {"class":"article-meta-value"}):
                    csv_content[0][2] =  ''.join(k.findAll(text=True)).encode('utf8')

    #append category
    for i in s.findAll('div', {"class":"article-metaline-right"}):
        for k in i.findAll('span', {"class":"article-meta-value"}):
            csv_content[0][4] = ''.join(k.findAll(text=True)).encode('utf8')
    
    csv_content[0][5] = DOCLINK + f  + '.txt'
    csv_content[0][6] = TEXTLINK + f + '.txt'
    #print csv_content
    
    # append the array into csv
    with open(SAVE_PATH + 'loadfile.txt', 'a') as fp: 
        a = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_ALL)
        a.writerows(csv_content)
        fp.close()

'''function for remove HTML tags'''
def removeHTML(filename, cnt):
    f = open(SAVE_PATH + 'native/' + OUTPUT_FILE_NAME + '%s.txt' % cnt, "w")
    soup = BeautifulSoup(open(filename), "html.parser")

    generateCSV(OUTPUT_FILE_NAME + '%s' % cnt, soup, filename)

    for div in soup.find_all("div", {'id':'topbar-container'}): 
        div.decompose()

    for div in soup.find_all("div", {'id':'navigation-container'}): 
        div.decompose()
    
    [item.extract() for item in soup.contents if isinstance(item, bs4.Doctype)]
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]

    for tag in invalid_tags: 
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    f.write(str(soup))
    f.flush()
    f.close()


    # copy native file to text folder
    copyfile(SAVE_PATH + 'native/' + OUTPUT_FILE_NAME + '%s.txt' % cnt, SAVE_PATH + 'text/' + OUTPUT_FILE_NAME + '%s.txt' % cnt)


''' main process start here!!!'''
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
os.makedirs(SAVE_PATH + '/native')
os.makedirs(SAVE_PATH + '/text')

for content in os.listdir(OPEN_PATH): # "." means current directory
    #print OPEN_PATH + content
    removeHTML(OPEN_PATH + content, cnt)
    cnt += 1

