# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import Config
from lib.ProxyIp import ProxyIp
import time
import os


class Main(object):
    def __init__(self):
        self.path = os.path.split(os.path.realpath(__file__))[0]
        self.enable_proxy = False
        self.wait_time = 5
        self.detail_total = 4  # visit 4 detail page

    def get_driver(self):
        executable_path = executable_path="%s/bin/chromedriver.exe" % self.path
        if self.enable_proxy:
            ip = {'Ip': '127.0.0.1', 'Port': 1080}
            proxy = '%s:%s' % (ip['Ip'], ip['Port'])
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument('--proxy-server=%s' % proxy)
            print 'Proxy:%s' % proxy
            return webdriver.Chrome(executable_path=executable_path, chrome_options=chromeOptions)
        else:
            return webdriver.Chrome(executable_path=executable_path)

    # dv driver; kw keyword; sp shop
    def search(self, dv, kw, sp):
        dv.maximize_window()
        print u'开始搜索： %s' % kw
        dv.get("http://www.taobao.com")
        dv.find_element_by_id("q").clear()
        dv.find_element_by_id("q").send_keys(kw)  # search
        dv.find_element_by_xpath('//form[@id="J_TSearchForm"]//button[@class="btn-search tb-bg"]').submit()
        return dv

    # search next page
    def next_page(self, dv, kw, sp):
        WebDriverWait(dv, self.wait_time).until(EC.title_contains(kw))
        self.scroll(dv)
        if not self.exist(dv, sp):
            print u'点击搜索下一页'
            dv.find_element_by_partial_link_text(u'下一页').click()
            self.next_page(dv, kw, sp)
        else:
            print u'此页有要找的宝贝！'
            items = dv.find_elements_by_xpath('//div[@id="mainsrp-itemlist"]//div[@class="item J_MouserOnverReq  "]')
            for item in items:
                try:
                    h = item.find_element_by_partial_link_text(sp)
                    a = item.find_element_by_xpath('.//a')
                    ActionChains(dv).move_to_element(h).click(a).perform()
                    self.switch_current(dv)
                    break
                except NoSuchElementException:
                    print u'这不是本店！'
                    continue
                except Exception as e:
                    # print e
                    continue

    def detail(self, dv, i):
        self.scroll(dv)
        WebDriverWait(dv, self.wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tshop-pbsm-shop-item-recommend')))
        dv.find_element_by_xpath(
            '//div[@class="skin-box tb-module tshop-pbsm tshop-pbsm-shop-item-recommend"]'
            '/div[@class="skin-box-bd"]/div[%s]' % i).click()
        self.switch_current(dv)

    # whether keyowrd exist or not.
    @staticmethod
    def exist(dv, kw):
        try:
            dv.find_element_by_partial_link_text(kw)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def scroll(dv):
        dv.execute_script("window.scrollBy(0, 700)")
        time.sleep(2)
        dv.execute_script("window.scrollBy(0, 700)")
        time.sleep(2)
        dv.execute_script("window.scrollBy(0, document.body.scrollHeight)")

    @staticmethod
    def switch_current(dv):
        for h in dv.window_handles:
            dv.switch_to.window(h)

    def main(self):
        for shop in Config.shops:
            for term in Config.terms:
                try:
                    driver = self.get_driver()
                    self.search(driver, term, shop)
                    self.next_page(driver, term, shop)
                    for i in range(1, self.detail_total + 1):
                        self.detail(driver, i)
                except Exception as e:
                    print e
                finally:
                    driver.quit()

Main().main()
