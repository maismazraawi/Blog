from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:mys0206887@localhost:5432/blogs'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)

SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
