"""Declares database classes and initializes engine and session"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float 
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


class OCR_Letter(Base):
	__tablename__ = 'ocr_letters'
	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer)
	file_url = Column(String(150))
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float) 

class Letter(Base):
	__tablename__ = 'letters'

	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer)
	file_url = Column(String(150))
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float)
	font_name = Column(String(100))

	font_id = Column(Integer, ForeignKey('fonts.id'))
	font = relationship('Font', backref=backref('fonts', order_by=id))


	
	# add an is serif column?	
class User_Image(Base):
	__tablename__ = 'user_images'

	id = Column(Integer, primary_key = True, autoincrement = True)
	file_url = Column(String(150))
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float)
	training_letter_aspect_ratio = Column(Float, ForeignKey('ocr_letters.aspect_ratio'))
	letter_aspect_ratio = Column(Float, ForeignKey('letters.aspect_ratio'))

	training_letter = relationship('OCR_Letter', backref=backref('ocr_letters', order_by=id))
	letter = relationship('Letter', backref = backref('letters', order_by=id))


def main():
	Base.metadata.create_all(engine)
	# change to pass after tables created the first time 

if __name__ == "__main__":
	main()


