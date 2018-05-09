# _*_ coding:utf-8 _*_

import csv


disease_dict = []


def main():
    with open('./csv_file/disease_list.csv') as f:
        dic = csv.DictReader(f)
        global disease_dict
        disease_dict = [x['DISEASE'] for x in dic]


def data_import():
    print(disease_dict)

    pass


if __name__ == '__main__':
    main()
