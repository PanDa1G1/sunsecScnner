# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
from scrapy.http import HtmlResponse
import random
from selenium.common import exceptions  
import sys
from colorama import Fore, Style, Back

class SuntestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SuntestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeleniumMiddleWare:

    def __init__(self):

        self.firefox_options=Options()
        self.firefox_options.headless = True
        self.browser = webdriver.Firefox(options=self.firefox_options)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60Opera/8.0 (Windows NT 5.1; U; en)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11']

    def relocatedTest(self,attr,value,url):

        try:        
            driver = webdriver.Firefox(options=self.firefox_options)
            driver.get(url)
            tag = driver.find_element_by_xpath('//*[@{}="{}"]'.format(attr,value))
            ActionChains(driver).move_to_element(tag).click(tag).perform()
            tempUrl = driver.current_url
            #print("[19]",tempUrl,sep="")
            if tempUrl == url:
                driver.close()
                return 1
            else:
                driver.close()
                return tempUrl
        except:
            driver.close()
            return 1

    def process_request(self,request,spider):
        self.browser.get(request.url)
        clickList = self.browser.find_elements_by_xpath("//*[@onclick]")
        mouseList = self.browser.find_elements_by_xpath("//*[@onmousemove]")
        #print("[12]",clickList,sep="")
        redirectUrls=[]
        try:
            if clickList:
                for tag in clickList:
                    attr = tag.get_attribute('onclick')
                    #print("[18]",attr,sep="")
                    result = self.relocatedTest("onclick",attr,request.url)
                    if result != 1:
                        clickList.remove(tag)
                        #print("[14]",result,sep="")
                        redirectUrls.append(result)
                #print("[11]",clickList,sep="")
                #print("[13]",redirectUrls,sep="")#模拟鼠标移动
        except exceptions.MoveTargetOutOfBoundsException as e:
            print("error")
            pass
        result = self.browser.page_source + "<div class='redir'>{}</div>".format(",".join(redirectUrls))
        #print("[5]"+result)
        #self.browser.close()
        return HtmlResponse(url=request.url,body=result,status=200,request=request,encoding="utf8")
