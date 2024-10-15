from app.database import accidents, parse_date
from flask import jsonify
from bson import json_util
import json


def get_accidents_by_area(beat):
    total = accidents.count_documents({'BEAT_OF_OCCURRENCE': beat})
    return jsonify({'beat': beat, 'total_accidents': total}), 200


def get_accidents_by_area_time(beat, period, start_date, end_date):
    query = {'BEAT_OF_OCCURRENCE': beat}
    if start_date and end_date:
        query['CRASH_DATE'] = {
            '$gte': parse_date(start_date),
            '$lte': parse_date(end_date)
        }

    total = accidents.count_documents(query)
    return jsonify({'beat': beat, 'period': period, 'total_accidents': total}), 200


def get_accidents_by_cause(beat):
    pipeline = [
        {'$match': {'BEAT_OF_OCCURRENCE': beat}},
        {'$group': {
            '_id': '$PRIM_CONTRIBUTORY_CAUSE',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}}
    ]
    results = list(accidents.aggregate(pipeline))
    return jsonify({'beat': beat, 'causes': results}), 200


def get_injury_stats(beat):
    pipeline = [
        {'$match': {'BEAT_OF_OCCURRENCE': beat}},
        {'$group': {
            '_id': None,
            'total_injuries': {'$sum': '$INJURIES_TOTAL'},
            'fatal_injuries': {'$sum': '$INJURIES_FATAL'},
            'incapacitating_injuries': {'$sum': '$INJURIES_INCAPACITATING'},
            'non_incapacitating_injuries': {'$sum': '$INJURIES_NON_INCAPACITATING'}
        }}
    ]
    result = list(accidents.aggregate(pipeline))[0]

    fatal_accidents = list(accidents.find({
        'BEAT_OF_OCCURRENCE': beat,
        'INJURIES_FATAL': {'$gt': 0}
    }))

    return jsonify({
        'beat': beat,
        'total_injuries': result['total_injuries'],
        'fatal_injuries': result['fatal_injuries'],
        'incapacitating_injuries': result['incapacitating_injuries'],
        'non_incapacitating_injuries': result['non_incapacitating_injuries'],
        'fatal_accidents': json.loads(json_util.dumps(fatal_accidents))
    }), 200
