from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

db_username = 'conduit'
db_password = 'conduit_password'
db_url = '127.0.0.1:3306'
db_name = 'conduitdb'

connectionString = (
    f'mysql+mysqldb://{db_username}:{db_password}@{db_url}/{db_name}'
)

# echo=True for debug
engine = create_engine(connectionString, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass