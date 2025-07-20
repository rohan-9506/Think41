from flask import Blueprint, request, jsonify
from app import db
from app.models import Poll, PollOption, VoteLog
from app.utils.redis_client import redis_client

vote_bp = Blueprint('vote', __name__)

@vote_bp.route('', methods=['POST'])
def cast_vote():
    data = request.get_json()
    poll_id = data['poll_id']
    option_id = data['option_id']
    user_id = data['user_id']

    # Prevent duplicate votes
    if VoteLog.query.filter_by(user_id=user_id, poll_id=poll_id).first():
        return jsonify({'error': 'User already voted'}), 400

    # Store vote in Redis
    redis_key = f'poll:{poll_id}:option:{option_id}'
    redis_client.incr(redis_key)

    # Log the vote in DB
    vote = VoteLog(user_id=user_id, poll_id=poll_id, option_id=option_id)
    db.session.add(vote)
    db.session.commit()

    return jsonify({'message': 'Vote cast'}), 200
