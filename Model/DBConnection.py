from configparser import ConfigParser
import psycopg2


# function read the DatabaseConnection.ini file and returns connection parameters.
def config(filename='./Model/DatabaseConnection.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


# function connects to the postgres database
def connect():
    """ Connect to the PostgreSQL database server """
    connection = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cursor.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')


# function to execute a query on database and return its value
def execute_query(input_query):
    try:
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        postgreSQL_select_Query = input_query

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows ")
        records = cursor.fetchall()
        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# function to write the result to database
def write_query(output_query, *record_to_insert):
    """Sample: INSERT INTO db (*columns) VALUES (%s)
        \n values can be set as empty and in single query"""
    try:
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        postgres_insert_query = output_query
        record_to_insert = record_to_insert
        if record_to_insert is not None:
            cursor.execute(postgres_insert_query, record_to_insert)
        elif record_to_insert is None:
            cursor.execute(postgres_insert_query)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully")


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# function to update database results
def update_query(update_query, *record_to_update):
    try:
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Update single record now
        #sql_update_query = """Update mobile set price = %s where id = %s"""
        sql_update_query = update_query
        records = record_to_update
        cursor.execute(sql_update_query, records)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    connect()
