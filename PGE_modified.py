from bs4 import BeautifulSoup
import requests
from pytz import timezone
import os

def modified():
    #import last date updated
    global last_date
    #scroll through pge.com and extract most recent date from relevant table
    browser = requests.get("http://www.pge.com/pipeline/operations/cgt_pipeline_status.page?#storage_activity")
    soup = BeautifulSoup(browser.content,'lxml')
    table = soup.find_all('table')[8]
    row = table.find_all('tr')[0]
    head = row.find_all('th')[3]
    date = 0
    for i in head:
        if isinstance(i, str):
            date = i
    #checks if new date which we just extracted is different from last seen updated date stored in text file last_date
    if last_date != date:
        #update last_date to newest updated date and run web crawler
        txt = open('C:\\Users\\...\\date.txt', 'w')
        txt.write(date)
        os.system('python C:\\...\\PGE_crawl.py')

if __name__ == '__main__':
    #import text file which contains string of last updated date from PGE.com
    txt = open('C:\\...\\date.txt', 'r')
    last_date = str(txt.read())
    txt.close()
    modified()
