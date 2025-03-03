from orm import mapper, engine
from table_mapper import start_mapping


def create_tables():
    mapper.metadata.create_all(bind=engine)

def drop_tables():
    mapper.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    start_mapping()
    drop_tables()
    create_tables()