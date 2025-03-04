from orm_tool import mapper, engine


def create_tables():
    mapper.metadata.create_all(bind=engine)

def drop_tables():
    mapper.metadata.drop_all(bind=engine)

