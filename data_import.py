# _*_ coding:utf-8 _*_

import csv
import sql_helper.oracle_helper as helper
import logging
import urllib.request as req


disease_dict = []


def main():
    with open('./csv_file/disease_list.csv') as f:
        dic = csv.DictReader(f)
        global disease_dict
        disease_dict = [x['DISEASE'] for x in dic]
        print(disease_dict)
    try:
        data_import()
        print('import success')
    except Exception as e:
        print(e)


def data_import():
    """ url 疾病列表导入 """
    pre_sql = 'select count(1) as cou from spider_disease_list where DISEASE_NAME = :d_name '
    sql = 'insert into spider_disease_list (ID, DISEASE_NAME, SIPIDER_URL, FLAG_DONE) VALUES ' \
          '(seq_spider_disease_id.nextval, :name, :url, :flag)'
    # param_dict = []
    for d_name in disease_dict:
        pre_param = {'d_name': d_name}
        data_param = {'name': d_name, 'url': '', 'flag': '0'}

        with helper.OracleHelper() as f:
            # 1. 每次导入一行
            cou = f.execute_query(pre_sql, pre_param)
            d_cou = cou.fetchone()[0]
            print('%s 数量: %s' % (d_name, d_cou))
            if d_cou <= 0:
                f.execute_sql(sql, data_param)
            # 2. 批量导入
            # f.execute_sql_many(sql, param_dict)


def insert_disease_list():

    pass


if __name__ == '__main__':
   main()
