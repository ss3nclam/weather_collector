from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app_core.settings import config


def create(config):
    db_cred = dict(config.items('DATABASE'))
    user, pswrd, host, port, db_name = [db_cred[key] for key in db_cred]
    return create_engine(f"postgresql+psycopg2://{user}:{pswrd}@{host}:{port}/{db_name}")


engine = create(config)
session = Session(engine)