import sqlalchemy as sq
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, ForeignKey('shop.id'), nullable=False)
    # PrimaryKeyConstraint(id_book, id_shop, name='quni')
    count = sq.Column(sq.Integer, nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, ForeignKey('publisher.id'))
    publisher = relationship(Publisher, backref='book')
    shop = relationship(Stock, backref='shop')


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)
    book = relationship(Stock, backref='book')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, ForeignKey('stock.id'))
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref='sale')


def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)