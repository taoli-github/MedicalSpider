# _*_ coding:utf-8 _*_
import cx_Oracle
import config.db


connection_str = config.db.main_connect_str


class OracleHelper:
    """ cx_Oracle 帮助类 """
    def __enter__(self):
        self.__db = cx_Oracle.connect(connection_str)
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__db.close()

    def execute_query(self, sql, params=None):
        """ 查询逻辑(有参和无参) """
        try:
            if params is None or params is '':
                result = self.__cursor.execute(sql)
            else:
                result = self.__cursor.execute(sql, params)
        except cx_Oracle.DatabaseError as err:
            raise err
        return result

    def execute_sql(self, sql, params=None):
        """ 增、删、改逻辑 """
        self.__db.begin()
        try:
            if params is None or params is '':
                result = self.__cursor.execute(sql)
            else:
                result = self.__cursor.execute(sql, params)
        except cx_Oracle.DatabaseError as err:
            self.__db.rollback()
            raise err

        self.__db.commit()

    def execute_sql_many(self, sql, params):
        """ 批量操作 """
        self.__db.begin()
        try:
            result = self.__cursor.executemany(sql, params)
        except cx_Oracle.DatabaseError as err:
            self.__db.rollback()
            raise err

        self.__db.commit()
