from pyramid.security import (
    Allow,
    Everyone,
    )

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data

class Author(Base):
    """ The SQLAlchemy declarative model class for a Author object. """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    kana = Column(Text)

    def __init__(self, name, kana):
        self.name = name
        self.kana = kana

class Book(Base):
    """ The SQLAlchemy declarative model class for a Book object. """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    title = Column(Text)
    question_id = Column(Integer)

    def __init__(self, author_id, title, question_id):
        self.author_id = author_id
        self.title = title
        self.question_id = question_id

class Criminal(Base):
    """ The SQLAlchemy declarative model class for a Book object. """
    __tablename__ = 'criminals'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    name = Column(Text)

    def __init__(self, book_id, title):
        self.book_id = book_id
        self.name = name

class Alias(Base):
    """ The SQLAlchemy declarative model class for a Alias object. """
    __tablename__ = 'aliases'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    name = Column(Text)

    def __init__(self, criminal_id, name):
        self.criminal_id = criminal_id
        self.name = name

class Question(Base):
    """ The SQLAlchemy declarative model class for a Question object. """
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    next = Column(Integer)

    def __init__(self, text, next):
        self.text = text
        self.next = next

class Answer(Base):
    """ The SQLAlchemy declarative model class for a Answer object. """
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    text = Column(Text)

    def __init__(self, question_id, text):
        self.question_id = question_id
        self.text = text
        
class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass
    
