# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from config import Config
from lib.ProxyIp import ProxyIp
import time
import os

path = os.path.split(os.path.realpath(__file__))[0]
enable_proxy = False
wait_time = 5
# ips = ProxyIp().get_proxy_ips() if enable_proxy else [1]
ips = [{'Ip': '127.0.0.1', 'Port': 1080}]

for ip in ips:
    for shop in Config.shops:
        for term in Config.terms:
            if enable_proxy:
                proxy = '%s:%s' % (ip['Ip'], ip['Port'])
                chromeOptions = webdriver.ChromeOptions()
                chromeOptions.add_argument('--proxy-server=%s' % proxy)
                print 'Proxy:%s' % proxy
                driver = webdriver.Chrome(executable_path="%s/bin/chromedriver.exe" % path, chrome_options=chromeOptions)
            else:
                driver = webdriver.Chrome(executable_path="%s/bin/chromedriver.exe" % path)
            driver.maximize_window()
            print 'Index Page %s' % shop
            driver.get("http://www.taobao.com")
            driver.find_element_by_id("q").clear()
            driver.find_element_by_id("q").send_keys(term)  # search
            driver.find_element_by_xpath('//form[@id="J_TSearchForm"]//button[@class="btn-search tb-bg"]').submit()

            try:
                WebDriverWait(driver, wait_time).until(EC.title_contains(term))
                for i in range(1, 5):
                    try:
                        time.sleep(wait_time)
                        print 'Search Result Page %s ' % driver.title
                        # driver.find_element_by_partial_link_text(shop).click()  # find shop and click, will create new tab.
                        items = driver.find_elements_by_xpath('//div[@id="mainsrp-itemlist"]//div[@data-category="personalityData"]')
                        i = 1
                        for item in items:
                            try:
                                shop_temp = item.find_element_by_partial_link_text(shop)
                                try:
                                    time.sleep(wait_time)
                                    f = item.find_element_by_xpath('.//a')
                                    print item
                                    item.click()
                                    # driver.find_element_by_xpath('//div[@class="items"]/div[%s]//a' % i).click()
                                    #item.find_element_by_css_selector('a').click()
                                    print 'Find it!'

                                    for handle in driver.window_handles:
                                        driver.switch_to.window(handle)
                                    for baby in Config.babies:
                                        print 'Shop Baby Page %s' % driver.title
                                        driver.find_element_by_partial_link_text(baby).click()
                                        time.sleep(wait_time)  # stop 1 minute
                                        driver.back()
                                except NoSuchElementException:
                                    print NoSuchElementException
                                break
                            except NoSuchElementException:
                                i += 1
                                print 'Next item %s' % i
                                if i >= 48:
                                    raise NoSuchElementException
                    except NoSuchElementException:
                        print 'Search Result Next Page %s' % driver.title
                        driver.find_element_by_partial_link_text(u'下一页').click()
                driver.close()
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
            finally:
                time.sleep(wait_time)
            driver.quit()
