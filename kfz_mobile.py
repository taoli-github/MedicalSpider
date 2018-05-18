# _*_ coding:utf-8 _*_

import urllib.request as request
import config.db
import sql_helper.oracle_helper as helper


def main():
    with helper.OracleHelper() as of:
        res = of.execute_query('select * from spider_disease_list where rownum < 11')
        for re in res:
            print(re)
    # req = request.Request('http://brain.kangfuzi.com')
    # req.add_header('User-Agent', config.db.windows_phone_user_agent)
    # print(request.urlopen(req).read().decode('utf-8'))


if __name__ == '__main__':
    main()
