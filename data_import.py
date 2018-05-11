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
    try:
        data_import()
        print('import success')
    except Exception as e:
        print(e)


def data_import():
    sql = 'insert into spider_disease_list VALUES ' \
          '(seq_spider_disease_id.nextval, :name, :url, :flag, 1)'
    param_dict = []
    for d_name in disease_dict:
        param_dict.append((d_name, 'http://brain.kangfuzi.com/jibing/'+req.quote(d_name), '0'))

    with helper.OracleHelper() as f:
        # 1. 每次导入一行
        # for d_name in disease_dict:
        #     str_sql = 'insert into spider_disease_list VALUES ' \
        #               '(seq_spider_disease_id.nextval, :name, :url, :flag)'
        #     params= {}
        #     params['name'] = d_name
        #     params['url'] = ''
        #     params['flag'] = '0'
        #     f.execute_sql(str_sql, params)
        # 2. 批量导入
        f.execute_sql_many(sql, param_dict)


if __name__ == '__main__':
   main()
