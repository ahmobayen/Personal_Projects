# libraries

from Model import DBConnection
from Model import NLProcess as Process

# variables
total_number = 0
dataFrame = {
    'post_id': [],
    'comment': [],
    'date': [],
    'username': [],
    'value': [],
    'polarity': []
}

# import data
try:
    import_query = 'select post_id, comment, date, username from socialmedia.raw_data_entry'
    output_query = 'insert into socialmedia.data_nlp_processed values (%s,%s,%s,%s)'
    result = DBConnection.execute_query(import_query)
    # process data
    for row in result:
        if row[1] != 'Caption':
            post_id = row[0]
            comment = row[1]
            date = row[2]
            username = row[3]
            value, polarity = Process.tweet_assessment(row[1])
            try:
                output = DBConnection.write_query(output_query, post_id, date, value, polarity)
            finally:
                total_number += 1
                print(total_number)
        else:
            total_number += 1
            print(total_number, 'Caption is Passed')
finally:
    print('Finished')
