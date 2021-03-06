# _*_ coding:utf-8 _*_

import urllib.request as request
import sql_helper.oracle_helper as helper
import time, random
from lxml import etree


spider_list = []
USER_AGENT_PC = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
USER_AGENT_MOBILE = ''


def main():
    get_disease_list()
    html_spider()


def html_spider():

    code_sql = 'insert into spider_source_code ' \
               'values (seq_spider_code_id.nextval, :d_id, :code, :flag_invalid, 0, 0, 0) '
    update_sql = 'update spider_disease_list set flag_done = 1 where id = :id '

    count = 0
    for ele in spider_list:
        # if count > 0:
        #     break

        d_id = ele[0]
        d_name = ele[1]
        d_url = ele[2]
        spider_name = ele[3]
        print('&&&&&&&&&&&&&&&&&&==================&&&&&&&&&&&&&&&&&&&&')
        print('正在解析url:%s, id:%s, name:%s' % (d_url, d_id, spider_name))

        html_code = ''

        req_url = 'http://brain.kangfuzi.com/jibing/' + request.quote(spider_name)
        req = request.Request(req_url)
        print(req_url)

        req.add_header('User-Agent', USER_AGENT_PC)
        try:
            with request.urlopen(req, timeout=5) as f:
                html_code = f.read().decode('utf-8')

            htmlc = etree.HTML(html_code)
            result = etree.tostring(htmlc)
            div_path = htmlc.xpath('//div')
            if len(div_path) == 0:
                print('无疾病百科')
                update_flag_wiki(d_id)
                continue

            params = {'d_id': d_id, 'code': result.decode('utf-8'), 'flag_invalid': '0'}
            update_param = {'id': d_id}
            with helper.OracleHelper() as oh:
                oh.execute_sql(code_sql, params)
                oh.execute_sql(update_sql, update_param)
        except Exception as e:
            print(e)
            # raise e
            continue

        time.sleep(random.randint(0, 10) * 2)
        count = count + 1
        print('解析完成url:%s, name:%s' % (d_url, d_name))
        print('&&&&&&&&&&&&&&&&&&==================&&&&&&&&&&&&&&&&&&&&')


def get_disease_list():
    sql = 'select id,disease_name,sipider_url,spider_name ' \
          'from spider_disease_list ' \
          'where flag_done = 0 and flag_invalid = 0 order by id '
    with helper.OracleHelper() as f:
        disease_list = f.execute_query(sql)

        for row in disease_list:
            spider_list.append(row)


def update_flag_wiki(id):
    wiki_sql = 'update spider_disease_list set flag_wiki = 0 where id = :id '
    with helper.OracleHelper() as f:
        f.execute_sql(wiki_sql, {'id': id})


update_html_code_sql = 'update spider_source_code set source_code = :source_code ' \
                        ' where id = 7140 '


def update_html_code_by_name(dis_name):
    req_url = 'http://brain.kangfuzi.com/jibing/' + request.quote(dis_name)
    req = request.Request(req_url)
    print(req_url)

    req.add_header('User-Agent', USER_AGENT_PC)
    try:
        with request.urlopen(req, timeout=5) as f:
            html_code = f.read().decode('utf-8')

        htmlc = etree.HTML(html_code)
        result = etree.tostring(htmlc)
        div_path = htmlc.xpath('//div')
        if len(div_path) == 0:
            print('无疾病百科')

        params = {'source_code': result.decode('utf-8')}

        with helper.OracleHelper() as oh:
            oh.execute_sql(update_html_code_sql, params)
    except Exception as e:
        print(e)
        # raise e


if __name__ == '__main__':
    # print(sys.getdefaultencoding())
    # print(sys.stdout.encoding)
    try:
        # main()
        update_html_code_by_name('窦性停搏')
    except Exception as e:
        print('error:', e)
        # raise e
