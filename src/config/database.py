import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_url = os.environ.get('DB_URL')
db_name = os.environ.get('DB_NAME')

connectionString = (
    f'mysql+mysqldb://{db_username}:{db_password}@{db_url}/{db_name}'
)

# echo=True for debug
engine = create_engine(connectionString)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass