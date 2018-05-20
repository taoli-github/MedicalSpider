# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from lxml import etree
import html
import time
import csv


def main():
    mobile_emulation = {'deviceName': 'iPhone 8 Plus'}
    chrome_options = Options()
    chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    try:
        # region 1. 百度搜索
        # browser.get('http://www.baidu.com')
        # input = browser.find_element_by_id('kw')
        # input.send_keys('Python')
        # input.send_keys(Keys.ENTER)
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
        # endregion
        browser.get('http://brain.kangfuzi.com')

        select_li = browser.find_elements(By.CSS_SELECTOR, '.list li')
        select_div = browser.find_element_by_css_selector('.nice-select')
        # print('select_li:%s' % len(select_li))

        dict_writer = []
        for sel_i in select_li:
            select_div.click()
            time.sleep(1)
            sel_i.click()
            time.sleep(3)

            source_code = browser.page_source
            html_code = etree.HTML(source_code)
            rev = parse_source_code(html_code)
            for i in rev:
                dict_writer.append(i)
            time.sleep(3)

        print(dict_writer)
        with open('./spider_result/symptom.csv', 'w', newline='') as f:
            header = ['sex', 'age', 'symptom', 'body_part']
            writer = csv.DictWriter(f, header)
            writer.writeheader()

            writer.writerows(dict_writer)
    finally:
        browser.close()


def parse_source_code(html_code):
    """ 解析源代码 """
    body_parts_span = html_code.xpath('//div[@class="body-parts"]/span/a/text()')
    sex_age = html_code.xpath('//div/span[@class="current"]/text()')
    sex = sex_age[0].split('|')[0]
    age = sex_age[0].split('|')[1]

    print('sex:%s, age:%s' % (sex, age))
    reval = []
    for i in range(1, len(body_parts_span) + 1):
        s_id = 'body-parts-tab' + str(i)
        body_part = body_parts_span[i - 1]
        symptom_list = html_code.xpath('//div[@id=\"' + s_id + '\"]/ul/li/a/text()')
        # print('%s:%s' % (body_part, symptom_list))
        for symptom in symptom_list:
            reval.append({'sex': sex, 'age': age, 'symptom': str_handle(symptom), 'body_part': body_part})

            # print('res:', res)
    return reval


def str_handle(string):
    return string.replace(' ', '')


if __name__ == '__main__':
    main()
