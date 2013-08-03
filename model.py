"""Declares database classes and initializes engine and session"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('sqlite:///fonts.db', echo=True)
session = scoped_session(sessionmaker(bind=engine,
									autocommit=False,
									autoflush=False))
# do I need session if I'm not going to be connecting to webapp?

Base = declarative_base()
Base.query = session.query_property()

# Class declarations
class Font(Base):
	__tablename__ = 'fonts'
	id = Column(Integer, primary_key = True, autoincrement = True)
	name = Column(String(100))
	family = Column(String(100))

class Trainer (Base):
	__tablename__ = 'trainers'
	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer)

class Letter(Base):
	__tablename__ = 'letters'

	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer(10)), ForeignKey('training_letters.value')
	file_url = Column(String(150))
	upper = Column(Boolean)
	height = Column(Integer)
	width = Column(Integer)

	font_id = Column(Integer, ForeignKey('fonts.id'))
	font_name = Column(String, ForeignKey('fonts.name'))

	# not sure how this works 
	font = relationship('Font', backref=backref('fonts', order_by=id))
	training_letter = relationship('Training', backref=backref('trainers', order_by=value))

	
	# add an is serif column?	

def main():
	Base.metadata.create_all(engine)
	# change to pass after tables created the first time 

if __name__ == "__main__":
	main()


