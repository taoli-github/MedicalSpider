# _*_ coding:utf-8 _*_

import urllib.request as request
import sys


def main():
    url = 'http://brain.kangfuzi.com/jibing/' + request.quote('肺炎')

    with request.urlopen(url) as f:
        print(f.read().decode('utf-8'))


if __name__ == '__main__':
    # print(sys.getdefaultencoding())
    # print(sys.stdout.encoding)
    main()
