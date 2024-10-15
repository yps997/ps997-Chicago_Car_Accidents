from pymongo import MongoClient
from flask import jsonify
import csv
import os
from datetime import datetime

client = None
db = None
accidents = None


def init_db(app):
    global client, db, accidents
    client = MongoClient(app.config['MONGO_URI'])
    db = client[app.config['DB_NAME']]
    accidents = db['accidents']


# def parse_date(date_string):
#     return datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%m/%d/%Y %H:%M')
    except ValueError:
        print(f"Unable to parse date: {date_string}")
        return None


def init_database():
    accidents.delete_many({})


def init_database():
    accidents.delete_many({})

    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                            'Traffic_Crashes_-_Crashes - 20k rows.csv')

    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row['CRASH_DATE'] = parse_date(row['CRASH_DATE'])

            for field in ['INJURIES_TOTAL', 'INJURIES_FATAL', 'INJURIES_INCAPACITATING', 'INJURIES_NON_INCAPACITATING']:
                row[field] = int(row[field]) if row[field] else 0

            accidents.insert_one(row)

    accidents.create_index('BEAT_OF_OCCURRENCE')
    accidents.create_index('CRASH_DATE')
    accidents.create_index('PRIM_CONTRIBUTORY_CAUSE')

    return jsonify({'message': 'Database initialized successfully'}), 200
