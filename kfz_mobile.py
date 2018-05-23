# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from lxml import etree
import html
import time
import csv


mobile_emulation = {'deviceName': 'iPhone 8 Plus'}
chrome_options = Options()
chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)


def main():
    try:
        # region 1. 百度搜索
        # browser.get('http://www.baidu.com')
        # input = browser.find_element_by_id('kw')
        # input.send_keys('Python')
        # input.send_keys(Keys.ENTER)
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
        # endregion
        browser = webdriver.Chrome(chrome_options=chrome_options)
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
    """ 解析源代码 症状 """
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


def co_main():
    """ 解析单症状的伴随症状及对应疾病"""
    try:
        csv_list = []
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get('http://brain.kangfuzi.com')

        # with open('h:/code.html', 'w', encoding='utf-8') as f:
        #     f.write(browser.page_source)

        # 性别年龄 下拉框div
        select_div = browser.find_element_by_css_selector('.nice-select')
        select_div.click()

        time.sleep(1)
        # 性别年龄 下拉框
        select_li = browser.find_element_by_xpath('//ul[@class="list"]/li[contains(text(), "女|成人")]')
        select_li.click()
        time.sleep(3)
        # 部位 span
        body_parts = browser.find_elements_by_css_selector('.body-parts span a')
        # 检验tab
        lis_tab = browser.find_elements_by_css_selector('.result-menu span a')

        time.sleep(3)
        """ 手机模式下 click 不起作用 采用 touchactions 需要查看源代码采用哪种触发方式 """
        # body_part[0].click()
        # region 绑定TouchAction
        # TouchActions(browser).tap(lis_tab[1]).perform()
        # time.sleep(2)
        # TouchActions(browser).tap(lis_tab[0]).perform()
        # time.sleep(2)
        # TouchActions(browser).tap(body_parts[1]).perform()
        # endregion
        for j in range(len(body_parts)):
            if j is not 5:
                continue
            TouchActions(browser).tap(body_parts[j]).perform()
            str_href = body_parts[j].get_attribute('href')
            part_id = str(str_href).split('com/')[1]
            print(part_id)
            time.sleep(3)
            # 对应症状
            symps_list = browser.find_elements_by_css_selector('#' + part_id + ' ul li a')
            for i in range(len(symps_list)):
                symptom = symps_list[i].text

                symps_list[i].click()
                time.sleep(3)
                html_code = etree.HTML(browser.page_source)
                res_li = html_code.xpath('//ul[@class="result-card"]/li/h2/text()')
                for res in res_li:
                    print(res)
                    print({'DISEASE': res, 'SYMPTOM': symptom})
                    csv_list.append({'DISEASE': res, 'SYMPTOM': symptom})

                res_modals = html_code.xpath('//div[@class="modal-body"]/ul/li/h2/text()')
                for m_res in res_modals:
                    print(m_res)
                    print({'DISEASE': m_res, 'SYMPTOM': symptom})
                    csv_list.append({'DISEASE': m_res, 'SYMPTOM': symptom})

                clean_tag = browser.find_element_by_id('clean-tags')
                TouchActions(browser).tap(clean_tag).perform()
                time.sleep(1)
                body_parts = browser.find_elements_by_css_selector('.body-parts span a')
                TouchActions(browser).tap(body_parts[j]).perform()
                time.sleep(1)

                symps_list = browser.find_elements_by_css_selector('#' + part_id + ' ul li a')
                time.sleep(2)
            body_parts = browser.find_elements_by_css_selector('.body-parts span a')
        time.sleep(2)

        with open('./spider_result/disease.csv', 'w', newline='') as f:
            header = ['SYMPTOM', 'DISEASE']
            writer = csv.DictWriter(f, header)
            writer.writeheader()

            writer.writerows(csv_list)
    finally:
        browser.close()


if __name__ == '__main__':
    # main()
    co_main()
