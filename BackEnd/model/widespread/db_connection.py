from configparser import ConfigParser
from os import path

# database connection drivers
import mysql.connector as mysql

from model.joint.static_paths import STATIC_PATH
from model.widespread.logger import Logger

# import psycopg2 as postgresql
# import cx_Oracle as oracle


class SqlDatabaseConnection:
    def __init__(self, connection=mysql, filename=path.join(STATIC_PATH, 'DatabaseConnection.ini'), section='my_sql'):
        """This method reads configuration files in order to make possible use different databases."""
        # Initialization Parameters
        self.select_result = []  # empty list uses for select queries.
        self.connection = connection  # for using different type of databases

        # Initialization Connection
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            params = parser.items(section)
            self.__db_info = {param[0]: param[1] for param in params}
            if connection == 'oracle':
                self.db = self.connection.connect('{user}/{password}@{host}'.format(user=self.__db_info['user'],
                                                  password=self.__db_info['password'], host=self.__db_info['host']))
            else:
                self.db = self.connection.connect(host=self.__db_info['host'], database=self.__db_info['database'],
                                                  user=self.__db_info['user'], password=self.__db_info['password'])
        else:
            raise Exception('Section {section} not found in the {file} file'.format(section=section, file=filename))
        self.cursor = self.db.cursor()
        self.logging = Logger('db_connection')

    def __delete__(self, instance):
        try:
            self.cursor.close()
            self.connection.close()
        finally:
            self.logging.info('Connection Closed Successfully')

    def commit_query(self, query=str, records_to_insert=tuple):
        """can execute All kind of queries required commit command such as: Import, Update, Delete
        Import single values and multiple values to database."""
        try:
            try:
                self.cursor.execute(query, records_to_insert)
            except:
                self.cursor.executemany(query, records_to_insert)
            finally:
                self.db.commit()
                self.logging.info(self.cursor.rowcount, 'record inserted.')

        except (Exception, self.connection.Error) as error:
            self.logging.error('Failed to insert record into {Database}'.format(Database=self.connection), error)

    def executive_query(self, query=str):
        """can execute All kind of queries doesn't need commit command such as: Select"""
        try:
            self.cursor.execute(query)
            self.select_result = self.cursor.fetchall()
            self.logging.info('query executed successfully')
        except (Exception, self.connection.Error) as error:
            self.logging.error('Error while Executing command on {Database}'.format(Database=self.connection), error)

    def get_result(self):
        return self.select_result


if __name__ == '__main__':
    item_list = (5, 1, '2020-01-01 05:05:05'), (2, 1, '2010-01-01 05:05:05'), (3, 1, '2030-01-01 05:05:05')
    # connect = SqlDatabaseConnection()
    # connect.executive_query('delete from slots')
    # connect.commit_query('insert into slots(id, status, time) values (%s, %s, %s)', item_list)
    # # connect.commit_query('insert into slots(id, status, time) values (%s, %s, %s)', (4, 1, '2010-01-01 05:05:05'))
    # connect.executive_query('select * from passage')
    # print(connect.get_result())
