import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DSN = f"postgresql://{os.getenv('POSTGRES_USER')}:"\
               f"{os.getenv('POSTGRES_PASSWORD')}@"\
               f"{os.getenv('POSTGRES_HOST', 'localhost')}:"\
               f"{os.getenv('POSTGRES_PORT')}/"\
               f"{os.getenv('POSTGRES_DB')}"

mapper = registry()
engine = create_engine(POSTGRES_DSN)
session_maker = sessionmaker(bind=engine)
