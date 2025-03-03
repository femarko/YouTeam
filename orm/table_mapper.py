import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from orm import mapper
from domain import models


user_table = Table(
    "user",
    mapper.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(200), nullable=False),
    Column("email", String(40), nullable=False, unique=True, index=True),
    Column("password", String(200), nullable=False),
    Column("creation_date", DateTime, server_default=func.now())
)


def start_mapping():
    mapper.map_imperatively(class_=models.User, local_table=user_table)
