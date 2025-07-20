from app.models import db, Poll, PollOption, VoteLog
from app.utils.redis_client import redis_client
from sqlalchemy.exc import IntegrityError

def cast_vote(poll_id, option_id, user_id=None):
    """
    Handles vote casting:
    - Checks if the poll and option are valid
    - Prevents duplicate voting if user_id is provided
    - Increments Redis vote count
    - Stores a VoteLog entry if user_id is provided
    """
    # Validate poll and option
    poll = Poll.query.filter_by(id=poll_id).first()
    option = PollOption.query.filter_by(id=option_id, poll_id=poll_id).first()

    if not poll or not option:
        return {"error": "Invalid poll or option"}, 400

    if poll.status != 'active':
        return {"error": "Poll is not active"}, 403

    # Check for duplicate vote
    if user_id:
        existing_vote = VoteLog.query.filter_by(poll_id=poll_id, user_id=user_id).first()
        if existing_vote:
            return {"error": "User has already voted"}, 409

    # Increment vote count in Redis
    redis_key = f"poll:{poll_id}:option:{option_id}:votes"
    redis_client.incr(redis_key)

    # Save vote log if user_id is provided
    if user_id:
        try:
            vote_log = VoteLog(poll_id=poll_id, option_id=option_id, user_id=user_id)
            db.session.add(vote_log)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Duplicate vote or DB error"}, 409

    return {"message": "Vote cast successfully"}, 200


def get_option_vote_count(poll_id, option_id):
    """
    Get the current vote count for an option from Redis.
    """
    redis_key = f"poll:{poll_id}:option:{option_id}:votes"
    return int(redis_client.get(redis_key) or 0)


def sync_votes_to_db(poll_id):
    """
    Optionally sync Redis counts to database (run as a scheduled job or admin action).
    """
    options = PollOption.query.filter_by(poll_id=poll_id).all()
    for option in options:
        redis_key = f"poll:{poll_id}:option:{option.id}:votes"
        redis_votes = int(redis_client.get(redis_key) or 0)
        option.vote_count = redis_votes
    db.session.commit()
