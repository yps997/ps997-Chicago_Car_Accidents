from flask import Blueprint, request, jsonify
from app.models import get_accidents_by_area, get_accidents_by_area_time, get_accidents_by_cause, get_injury_stats
from app.database import init_database

bp = Blueprint('main', __name__)

@bp.route('/init_database', methods=['POST'])
def init_db_route():
    return init_database()

@bp.route('/accidents_by_area/<beat>', methods=['GET'])
def accidents_by_area_route(beat):
    return get_accidents_by_area(beat)

@bp.route('/accidents_by_area_time/<beat>/<period>', methods=['GET'])
def accidents_by_area_time_route(beat, period):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return get_accidents_by_area_time(beat, period, start_date, end_date)

@bp.route('/accidents_by_cause/<beat>', methods=['GET'])
def accidents_by_cause_route(beat):
    return get_accidents_by_cause(beat)

@bp.route('/injury_stats/<beat>', methods=['GET'])
def injury_stats_route(beat):
    return get_injury_stats(beat)
