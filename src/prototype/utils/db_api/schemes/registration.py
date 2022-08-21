from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)
    client_fio = Column(String(200))
    quest_fio = Column(String(200))
    start_date = Column(String(30))
    validity = Column(String(30))
    status = Column(String(25))

    query: sql.select
