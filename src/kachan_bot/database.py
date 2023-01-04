from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(
    engine,
    autocommit=True,
    autoflush=True,
    expire_on_commit=False
)


def use_session(func):
    def _wrapper(*args, **kwargs):
        session = Session()
        result = func(*args, **kwargs, session=session)
        session.close()
        return result

    return _wrapper
