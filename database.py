from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String

# Replace 'sqlite:///rfg.db' with your path to database
engine = create_engine('sqlite:///rfg.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	email = Column(Text)
	username = Column(String(255))
