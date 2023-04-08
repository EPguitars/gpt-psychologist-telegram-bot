# pylint: disable=broad-exception-caught
"""
All operations with db in this module 
SQLAlchemy used as orm
"""
import json
import ast

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine.url import URL
from sqlalchemy import select

Session = orm.sessionmaker()

DATABASE = {
    'drivername': 'sqlite',
    'database': 'database.db'
}

engine = sa.create_engine(URL.create(**DATABASE))
Base = orm.declarative_base()

with open("behavior_prompts.json", "r", encoding="utf-8") as prompts:
    first_data = json.load(prompts)


class UserTable(Base):
    """
    Mapper for table "user"
    """
    __table__ = sa.Table('user', Base.metadata, autoload_with=engine)


def current_data(user_id: int) -> list:
    """
    This function gets users data from db
    """
    session = Session(bind=engine)
    dbdata = json.dumps(first_data)

    # Checking if user is already in db
    if session.query(UserTable.id).filter_by(id=user_id).first() is None:
        try:
            new_user = UserTable(id=user_id, data=dbdata)
            session.add(new_user)

            session.commit()
            print("NEW USER NOW USING BOT")

        except Exception:
            session.rollback()
            print("ERROR DATA ADDING TO DB " + Exception)

    dbdata = select(UserTable).where(UserTable.id == user_id)
    result = [x.data for x in session.scalars(dbdata)]
    session.close()
    data = ast.literal_eval(*result)

    return data


def update_db(user_id: int, data: list):
    """
    This function updates db with new dialogue
    """
    session = Session(bind=engine)

    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    user.data = str(data)

    session.commit()
    session.close()
