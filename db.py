from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./blog.db', echo=True)
Base = declarative_base()

class usertable(Base):
    __tablename__='usertable'
    __table_args__ = {'sqlite_autoincrement':True}
    userid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    passwd = Column(String, nullable=False)

class blogtable(Base):
    __tablename__='blogtable'
    __table_args__ = {'sqlite_autoincrement':True}
    blogid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)

def create_table():
    Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

