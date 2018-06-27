# _*_ coding: utf-8 _*_

import html
import sql_helper.oracle_helper as helper
from lxml import etree
import urllib.request as request
import time, random


def main():
    """ 解析用药tab """
    res = get_disease_code()
    disease_parser(res)


def get_disease_code():
    """ get html source code """
    code_sql = ''' select DISEASE_ID, SOURCE_CODE
                from spider_source_code where id > 2000
                 order by id '''

    list_r = []
    with helper.OracleHelper() as oh:
        result = oh.execute_query(code_sql)

        for r in result.fetchall():
            print(r[0], type(r[1].read()))
            if r[0] == 7140:
                continue

            list_r.append([r[0], r[1].read().encode('utf8')])

    return list_r


def disease_parser(res):
    """ 解析疾病源代码里的药品列表 """
    count = 0
    drug_list = []
    for item in res:
        disease_id = item[0]
        htmlc = etree.HTML(html.unescape(item[1].decode('utf-8')))
        # html_str = etree.tostring(htmlc)
        # yaopin
        home_div = htmlc.xpath('//html/body/div/div[@id="pharmacy"]/div[@class="result-box"]/div/div')
        print('==========')
        for ele in home_div:
            count += 1
            ele_str = html.unescape(etree.tostring(ele).decode('utf-8'))
            drug_p = etree.HTML(ele_str).xpath('//div/p/text()')
            drug_p.insert(0, disease_id)
            print(drug_p)
            drug_list.append(drug_p)
        print('==========')
    # print(drug_list)
    print(count)
    # drug_import(drug_list)


drug_pre_sql = 'select id from spider_drug_list ' \
                    'where drug_name = :drug_name '
drug_insert_sql = 'insert into spider_drug_list (id, drug_name, drug_brief, flag_done, flag_invalid) ' \
                      'values(seq_spider_drug_id.nextval, :drug_name, :drug_brief, 0, 0) '
disease_vs_drug_sql = 'insert into spider_disease_vs_drug (ID, DISEASE_ID, DRUG_ID,FLAG_INVALID) ' \
                      'values (seq_spider_dis_vs_drug_id.nextval, :dis_id, :drug_id, 0)'
disease_flag_drug_sql = 'update spider_source_code set flag_drug = \'1\' ' \
                        'where disease_id = :dis_id '


def drug_import(drug_list):
    """ 导入疾病列表 """
    for drug in drug_list:
        disease_id = drug[0]
        drug_name = code_replace(drug[1])
        drug_brief = code_replace(drug[2])
        print('*****************************************')
        print('药品:%s 疾病:%s' % (drug_name, disease_id))
        with helper.OracleHelper() as oh:
            res = oh.execute_query(drug_pre_sql, {'drug_name': drug_name})
            row_num = res.fetchone()
            print('是否存在:%s' % row_num)
            if row_num is not None:
                print('%s已存在此药，dis_id:%s,drug_name:%s,drug_id:' % (disease_id, drug_name, row_num[0]))
                oh.execute_sql(disease_vs_drug_sql, {'dis_id': disease_id, 'drug_id': row_num[0]})
            else:
                print('简介:', drug_brief)
                oh.execute_sql(drug_insert_sql, {'drug_name': drug_name, 'drug_brief': drug_brief})
                drug_id = oh.execute_query(drug_pre_sql, {'drug_name': drug_name})
                oh.execute_sql(disease_vs_drug_sql, {'dis_id': disease_id, 'drug_id': drug_id.fetchone()[0]})
            oh.execute_sql(disease_flag_drug_sql, {'dis_id': disease_id})
        print('********************************************')


def code_replace(string):
    return string.replace(u'\xa0 ', u' ').replace('\xa0', ' ').replace('\ue006','').replace(u'\ue006', u'').replace('\ue003','').replace(u'\ue003',u'').replace('\ue001','').replace(u'\ue001',u'').replace('\ue456','').replace(u'\ue456',u'').replace('\ue000','').replace(u'\ue000',u'').replace('\ue005','').replace(u'\ue005', u'').replace('0xaa', '')


drug_list_sql = 'select id, drug_name from spider_drug_list where flag_done = 0 and flag_invalid= 0 order by id'
drug_code_insert_sql = 'insert into spider_drug_source_code (id,drug_id,source_code,flag_parse,flag_invalid) ' \
                       'values(SEQ_SPIDER_DRUG_CODE_ID.Nextval, :drug_id, :source_code, 0, 0) '
drug_flag_done_up_sql = 'update spider_drug_list set flag_done = 1 ' \
                        'where id= :id '
drug_list = []
USER_AGENT_PC = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'


def drug_main():
    get_drug_list()
    drug_spider()


def drug_spider():
    for ele in drug_list:
        drug_id = ele[0]
        drug_name = ele[1]
        print('=====================')
        print('开始爬取: %s' % drug_name)
        drug_url = 'http://brain.kangfuzi.com/yaopin/' + request.quote(drug_name)
        print('药品url:%s' % drug_url)
        req = request.Request(drug_url)
        req.add_header('User-Agent', USER_AGENT_PC)
        try:
            with request.urlopen(req, timeout=5) as f:
                html_code = f.read().decode('utf-8')

                htmlc = etree.HTML(html_code)
                result = etree.tostring(htmlc)
                div_path = htmlc.xpath('//div')
                if len(div_path) == 0:
                    print('无药品说明')
                    continue
                with helper.OracleHelper() as oh:
                    oh.execute_sql(drug_code_insert_sql,{'drug_id': drug_id,'source_code': result.decode('utf-8')})
                    oh.execute_sql(drug_flag_done_up_sql, {'id': drug_id})
        except Exception as e:
            print(e)
            continue
        time.sleep(random.randint(0,10) * 2)
        print('*****************爬取完毕******************')


def get_drug_list():
    with helper.OracleHelper() as oh:
        result = oh.execute_query(drug_list_sql)
        for r in result:
            drug_list.append(r)


if __name__ == '__main__':
    # drug_main()
    main()
