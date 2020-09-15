## initialize.py
## Insert drama.json to MySQL database

import json
import MySQLdb



def connect_to_db():
    global connection
    global cursor

    connection = MySQLdb.connect(
        user="scrapingman",
        passwd="myPassword-1",
        host="localhost",
        db="scrapingdata",
        charset="utf8")

    cursor=connection.cursor()


def unconnect_to_db():
    connection.commit()
    connection.close()


def save_to_db():
    with open('drama.json') as json_file:
        json_data = json.load(json_file)

        json_array = json_data['drama2020']
        for i in range(len(json_array)):
            try:
                cursor.execute("INSERT INTO drama_info(drama_name, channel, start_time, start_day) values (%s, %s, %s, %s)", (json_array[i]['drama_name'], json_array[i]['channel'], json_array[i]['start_time'], json_array[i]['start_day']))
            except Exception as e:
                print(e)
        
        json_array = json_data['drama2019']
        for i in range(len(json_array)):
            try:
                cursor.execute("INSERT INTO drama_info(drama_name, channel, start_time, start_day) values (%s, %s, %s, %s)", (json_array[i]['drama_name'], json_array[i]['channel'], json_array[i]['start_time'], json_array[i]['start_day']))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    connect_to_db()
    save_to_db()
    unconnect_to_db()