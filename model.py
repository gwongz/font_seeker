"""Declares database classes and initializes engine and session"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float 
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('sqlite:///fonts.db', echo=True)
session = scoped_session(sessionmaker(bind=engine,
									autocommit=False,
									autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

class Font(Base):
	__tablename__ = 'fonts'
	id = Column(Integer, primary_key = True, autoincrement = True)
	name = Column(String(100))

class OCR_Letter(Base):
	__tablename__ = 'ocr_letters'
	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer)
	file_url = Column(String(150))
	black_pixels = Column(Integer)
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float)

class Letter(Base):
	__tablename__ = 'letters'

	id = Column(Integer, primary_key = True, autoincrement = True)
	value = Column(Integer)
	file_url = Column(String(150))
	black_pixels = Column(Integer)
	font_name = Column(String(100))
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float)


	font_id = Column(Integer, ForeignKey('fonts.id'))
	font = relationship('Font', backref=backref('fonts', order_by=id))


class User_Image(Base):
	__tablename__ = 'user_images'

	id = Column(Integer, primary_key = True, autoincrement = True)
	file_url = Column(String(150))
	width = Column(Integer)
	height = Column(Integer)
	aspect_ratio = Column(Float)
	black_pixels = Column(Integer)

	ocr_letter_black_pixels = Column(Integer, ForeignKey('ocr_letters.black_pixels'))
	letter_black_pixels = Column(Integer, ForeignKey('letters.black_pixels'))

	ocr_letter = relationship('OCR_Letter', backref=backref('ocr_letters', order_by=id))
	letter = relationship('Letter', backref = backref('letters', order_by=id))


def main():
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	main()


