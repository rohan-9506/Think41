from flask import Blueprint, request, jsonify
from app import db
from app.models import Poll, PollOption
from datetime import datetime

poll_bp = Blueprint('poll', __name__)

@poll_bp.route('', methods=['POST'])
def create_poll():
    data = request.get_json()
    poll = Poll(poll_str_id=data['poll_str_id'], question=data['question'])
    db.session.add(poll)
    db.session.flush()  # Get poll.id before commit

    for opt in data['options']:
        option = PollOption(option_str_id=opt['option_str_id'], text=opt['text'], poll_id=poll.id)
        db.session.add(option)

    db.session.commit()
    return jsonify({'message': 'Poll created'}), 201

@poll_bp.route('/active', methods=['GET'])
def get_active_polls():
    polls = Poll.query.filter_by(is_active=True).all()
    result = [{'poll_str_id': p.poll_str_id, 'question': p.question} for p in polls]
    return jsonify(result)

@poll_bp.route('/<poll_str_id>/close', methods=['PATCH'])
def close_poll(poll_str_id):
    poll = Poll.query.filter_by(poll_str_id=poll_str_id).first()
    if not poll:
        return jsonify({'error': 'Not found'}), 404

    poll.is_active = False
    poll.end_time = datetime.datetime()
    db.session.commit()
    return jsonify({'message': 'Poll closed'})
