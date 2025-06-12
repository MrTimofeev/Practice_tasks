from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Genre(Base):
    __tablename__ = "genre"
    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String)
    
    book =  relationship("Book", back_populates="genre")


class Author(Base):
    __tablename__ = "author"
    autor_id = Column(Integer, primary_key=True)
    name_author = Column(String)
    
    book = relationship("Book", back_populates="author")


class City(Base):
    __tablename__ = "city"
    city_id = Column(Integer, primary_key=True)
    name_city = Column(String)
    days_delivery = Column(Integer)
    
    client = relationship("Client", back_populates="city")


class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('author.autor_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Integer)
    amount = Column(Integer)
    
    genre = relationship("Genre", back_populates="book")
    author = relationship("Author", back_populates="book")
    buy_book = relationship("Buy_book", back_populates="book")


class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True)
    name_client = Column(String)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String)
    
    
    city = relationship("City", back_populates="client")
    buy = relationship("Buy", back_populates="client")


class Buy(Base):
    __tablename__ = "buy"
    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String)
    client_id = Column(Integer, ForeignKey("client.client_id"))
    
    client = relationship("Client", back_populates="buy")
    buy_step = relationship ("Buy_step", back_populates="buy")
    buy_book = relationship("Buy_book", back_populates="buy")


class Step(Base):
    __tablename__ = "step"
    step_id = Column(Integer, primary_key=True)
    name_step = Column(String)
    
    buy_step = relationship("Buy_step", back_populates="step")


class Buy_book(Base):
    __tablename__ = "buy_book"
    buy_book_id = Column(Integer, primary_key=True)

    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))

    amount = Column(Integer)

    buy = relationship("Buy", back_populates="buy_book")
    book = relationship("Book", back_populates="buy_book")

class Buy_step(Base):
    __tablename__ = "buy_step"

    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))

    date_step_beg = Column(DateTime)
    date_step_end = Column(DateTime)

    buy = relationship("Buy", back_populates="buy_step")
    step = relationship("Step", back_populates="buy_step")