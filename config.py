class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/live_poll_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = 'redis://localhost:6379/0'
