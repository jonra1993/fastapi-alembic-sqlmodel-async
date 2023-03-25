from typing import Generator
from celery_sqlalchemy_scheduler.session import SessionManager
from app.core.config import settings

def get_job_db() ->Generator:
    try:
        session_manager = SessionManager()
        engine, _session = session_manager.create_session(settings.SYNC_CELERY_BEAT_DATABASE_URI)
        session = _session()
        return session
    finally:
        session.close()