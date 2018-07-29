# -*- coding:utf-8 -*-
import re
import requests
import mylogging
from bs4 import BeautifulSoup

crawlLogger = mylogging.MyLogger("crawler")

def get_html(url):
    crawlLogger.debug('get_html')
    _html = ""

    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def getTitle(bsObj):
    crawlLogger.debug('getTitle')
    try:
        title = bsObj.find("h1", {"class": "title"}).text.strip()
        return title

    except Exception as e:
        crawlLogger.error(e)
        return None


def getImage(bsObj):
    try:
        fullImageUrl = ""
        crawlLogger.debug('getImage')
        imgPattern = re.compile('^(파일:)(?!나무위키).*?$')
        for imageUrl in bsObj.findAll("img", {"data-src": re.compile('^(//cdn.namuwikiusercontent.com)(.*?)$')}):
            if imgPattern.search(imageUrl.attrs['alt']):
                fullImageUrl = 'https:' + imageUrl.attrs['data-src']
                break

        return fullImageUrl

    except Exception as e:
        crawlLogger.error(e)
        return None


def getEditDate(bsObj):
    try:
        crawlLogger.debug('getEditDate')
        editDate = bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
        return editDate

    except Exception as e:
        crawlLogger.error(e)
        return None


def getContent(bsObj):
    try:
        crawlLogger.debug('getContent')
        content = bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
        content = re.sub(r'\s{2,}', ' ', content)
        return content

    except Exception as e:
        crawlLogger.error(e)
        return None


def getCrawl(pageUrl):
    try:
        crawlLogger.debug('getCrawl')
        fullPageUrl = "https://namu.wiki" + pageUrl
        html = get_html(fullPageUrl)
        bsObj = BeautifulSoup(html, 'html.parser')

        if bsObj == None:
            return None
        title = getTitle(bsObj)
        content = getContent(bsObj)
        editDate = getEditDate(bsObj)
        image = getImage(bsObj)
        dbTuple = (title, fullPageUrl, content, image, editDate, html)

        return dbTuple

    except Exception as e:
        crawlLogger.error(e)


# def updateCrawl(pageUrl):
#     fullPageUrl = "https://namu.wiki" + pageUrl
#     html = get_html(fullPageUrl)
#     bsObj = BeautifulSoup(html, 'html.parser')
#
#     if bsObj == None:
#         return None
#
#     try:
#         title = getTitle(bsObj)
#         mylogger.debug(title, 'updateCrawl - title')
#         content = getContent(bsObj)
#         mylogger.debug(content, 'updateCrawl - content')
#         editDate = getEditDate(bsObj)
#         mylogger.debug(editDate, 'updateCrawl - editdate')
#         image = getImage(bsObj)
#         mylogger.debug(image, 'updateCrawl - image')
#         updateNamuwikiId = editDateUpdated(pageUrl, editDate)
#         if updateNamuwikiId > 0:
#             dbTuple = (pageUrl, title, content, image, editDate, htmlTxt, updateNamuwikiId)
#             updateNamuwikiDB(dbTuple)
#             print
#             "update DB"
#
#     except Exception as e:
#         mylogger.error(e, 'updateCrawl Error')
#     return


if __name__ == '__main__':
    insertUrls(['/w/'])
    getCrawl('/w/')

    # while True:
    #     try:
    #         for pageUrl in selectUncrawledUrl():
    #             try:
    #                 getCrawl(pageUrl)
    #
    #             except:
    #                 print
    #                 "getCrawl Error", type(e)
    #                 updateUrlState(pageUrl, "error")
    #             time.sleep(3)
    #
    #     except Exception as e:
    #         print
    #         "selectUncrawledUrl Error", type(e)
    #
    #     try:
    #         print
    #         "update DB"
    #         for scrapedUrl in selectScrapedUrl():
    #             try:
    #                 updateCrawl(scrapedUrl)
    #             except:
    #                 print
    #                 "updateCrawl Error", type(e)
    #                 updateUrlState(pageUrl, "error")
    #             time.sleep(3)
    #     except Exception as e:
    #         print
    #         "selectScrapedUrl Error", type(e)
    #
    #
