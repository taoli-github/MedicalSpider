# _*_ coding:utf-8 _*_

import urllib.request as request
import sql_helper.oracle_helper as helper
import time, random
from lxml import etree


spider_list = []
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'


def main():
    get_disease_list()
    html_spider()


def html_spider():

    code_sql = 'insert into spider_source_code ' \
               'values (seq_spider_code_id.nextval, :d_id, :code, :flag_invalid) '

    count = 0
    for ele in spider_list:
        if count > 0:
            break

        d_id = ele[0]
        d_name = ele[1]
        d_url = ele[2]

        html_code = ''
        req = request.Request(d_url)
        req.add_header('User-Agent', USER_AGENT)
        try:
            with request.urlopen(req, timeout=5) as f:
                html_code = f.read().decode('utf-8')

            html = html.par
            with helper.OracleHelper() as oh:
                pass


        except Exception as e:
            print(e)
            raise e
            continue

        time.sleep(random.randint(0,10) * 2)
        count = count + 1


def get_disease_list():
    sql = 'select id,disease_name,sipider_url ' \
          'from spider_disease_list ' \
          'where flag_done = 0 order by id '
    with helper.OracleHelper() as f:
        disease_list = f.execute_query(sql)

        for row in disease_list:
            spider_list.append(row)


if __name__ == '__main__':
    # print(sys.getdefaultencoding())
    # print(sys.stdout.encoding)
    try:
        main()
    except Exception as e:
        print('error:', e)
        raise e
