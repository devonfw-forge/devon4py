from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create an engine
# engine = create_engine('mysql+mysqldb://root:NEW_USER_PASSWORD@localhost:5432/order_mock')
#@ engine = create_engine('mysql://root:NEW_USER_PASSWORD@localhost/sqlalchemy3')


def make_engine(db_server, user, pw, host, db_name):
    engine = create_engine(f'{db_server}://{user}:{pw}@{host}/{db_name}')
    return engine

engine = make_engine(
    db_server="mysql",
    user = "root",
    pw = "NEW_USER_PASSWORD",
    host = "localhost",
    db_name = "sqlalchemy"
)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()




Base = declarative_base()