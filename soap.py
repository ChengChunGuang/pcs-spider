import requests
import re
import time
from lxml import etree

WEBSITE_TO_START=r"https://8zt.cc"
CUPS_OF_SOAP={}

def deal_with_single_result(page,soap):
    CUPS_OF_SOAP[page]=re.sub('\s', '', soap)

def deal_with_single_page(page):
    r=requests.get(page)
    if ( not r ) or r.status_code != 200 :
        return None

    tree=etree.HTML(r.content)
    thiz = tree.xpath('//*[@id="sentence"]')
    for item in thiz:
        if item.text:
            deal_with_single_result(page,item.text)

    next=tree.xpath("/html/body/div[3]/div/div/div/span/a")
    for item in next:
        anchor=item.get("href")
        if anchor:
            return WEBSITE_TO_START+anchor
    return next

def post_action_of_single_page(count):
    if count % 10 ==0:
        print('.'+str(count))
    else:
        print(".", end='')
    time.sleep(0.1)

def run():
    next_page=WEBSITE_TO_START
    count=0
    while(next_page):
        next_page=deal_with_single_page(next_page)
        count+=1
        if(count>2000):
            print("\nstopping....")
            break
        post_action_of_single_page(count)

    for item in CUPS_OF_SOAP.keys():
        print(item +","+CUPS_OF_SOAP[item])

if __name__ == '__main__' :
    run()
