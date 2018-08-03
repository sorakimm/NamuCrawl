# -*- coding:utf-8 -*-
import re
import requests
import mylogging
import db
from bs4 import BeautifulSoup
import enum
import db

crawlLogger = mylogging.MyLogger("crawler")



def get_html(url):
    crawlLogger.info('get_html : ' + url)
    _html = ""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            _html = resp.text

    except requests.exceptions.RequestException as e:
        crawlLogger.error(e + "url : " + url)
    return _html


def getTitle(bsObj):
    try:
        title = bsObj.find("h1", {"class": "title"}).text.strip()
        crawlLogger.info('getTitle : ' + title)
        return title

    except Exception as e:
        crawlLogger.error(e + "title : " + title)
        return None


def getImage(bsObj):
    try:
        fullImageUrl = ""
        imgPattern = re.compile('^(파일:)(?!나무위키).*?$')
        for imageUrl in bsObj.findAll("img", {"data-src": re.compile('^(//cdn.namuwikiusercontent.com)(.*?)$')}):
            if imgPattern.search(imageUrl.attrs['alt']):
                fullImageUrl = 'https:' + imageUrl.attrs['data-src']
                crawlLogger.info('getImage : ' + fullImageUrl)
                break

        return fullImageUrl

    except Exception as e:
        crawlLogger.error(e)
        return None


def getEditDate(bsObj):
    try:
        editDate = bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
        crawlLogger.info('getEditDate : ' + editDate)
        return editDate

    except Exception as e:
        crawlLogger.error(e + "editdate : " + editDate)
        return None


def getContent(bsObj):
    try:
        content = bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
        content = re.sub(r'\s{2,}', ' ', content)
        crawlLogger.info('getContent')
        return content

    except Exception as e:
        crawlLogger.error(e)
        return None


def getCrawl(pageUrl):
    try:
        crawlLogger.info('getCrawl')
        fullPageUrl = "https://namu.wiki" + pageUrl
        html = get_html(fullPageUrl)
        bsObj = BeautifulSoup(html, 'html.parser')

        if bsObj == None:
            return None
        title = getTitle(bsObj)
        content = getContent(bsObj)
        editDate = getEditDate(bsObj)
        image = getImage(bsObj)
        dbTuple = (title, fullPageUrl, content, image, editDate, html, fullPageUrl)
        db.insertNamuwikiDB(dbTuple)


        linkSet = set()
        crawlLogger.debug(linkSet)
        for link in bsObj.findAll("a", href=re.compile("^(/w/)((?!:).)*?$")):
            linkSet.add(link.get('href'))

        return linkSet

    except Exception as e:
        crawlLogger.error(dbTuple)


