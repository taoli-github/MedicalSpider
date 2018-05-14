# _*_ coding: utf-8 _*_

import html
import sql_helper.oracle_helper as helper
from lxml import etree


def main():
    res = get_disease_code()
    disease_parser(res)


def get_disease_code():
    """ get html source code """
    code_sql = ''' select DISEASE_ID, SOURCE_CODE
                from spider_source_code 
                 WHERE FLAG_INVALID = 0 AND flag_drug = 0 
                 AND DISEASE_ID in (1)
                 order by id '''

    list_r = []
    with helper.OracleHelper() as oh:
        result = oh.execute_query(code_sql)

        for r in result.fetchall():
            list_r.append([r[0], r[1].read().encode('utf-8')])

    return list_r


def disease_parser(res):
    count = 0
    drug_list = []
    for item in res:
        disease_id = item[0]
        htmlc = etree.HTML(html.unescape(item[1].decode('utf-8')))
        # html_str = etree.tostring(htmlc)
        # 常识
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
    print(drug_list)
    print(count)
    drug_import(drug_list)


drug_pre_sql = 'select id from spider_drug_list ' \
                    'where drug_name = :drug_name'
drug_insert_sql = 'insert spider_drug_list (id, drug_name, drug_brief, flag_done, flag_invalid) ' \
                      'values(seq_spider_drug_id.nextval, :drug_name, :drug_brief, 0, 0) '


def drug_import(drug_list):
    """ 导入疾病列表 """
    for drug in drug_list:
        disease_id = drug[0]
        drug_name = drug[1]
        drug_brief = drug[2]
        with helper.OracleHelper() as oh:
            count = oh.execute_query(drug_pre_sql, 'hi')
            print(count.fetchone()[0])


if __name__ == '__main__':
    main()
