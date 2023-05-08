import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from models import Publisher, Book, Shop, Stock, Sale, create_table


def add_data(session):
    with open('data.json', 'r') as db:
        data = json.load(db)

    for record in data:
        model = {'publisher': Publisher,
                 'shop': Shop,
                 'book': Book,
                 'stock': Stock,
                 'sale': Sale
                 }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def find_info_by_publisher(session, publisher=None):
    if publisher.isdigit():
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale
        ).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == publisher).all():
            print(f'{c[0]} | {c[1]} | {c[2]} | {c[3]}')
    else:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale
        ).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name.ilike(f'%{publisher}%')).all():
            print(f'{c[0]} | {c[1]} | {c[2]} | {c[3]}')


if __name__ == '__main__':
    db_user = os.getenv("db_user")
    db_pass = os.getenv("db_pass")
    db_name = os.getenv("db_name")
    DSN = f"postgresql://{db_user}:{db_pass}@localhost:5432/{db_name}"

    engine = sqlalchemy.create_engine(DSN)

    create_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    add_data(session)

    publisher = input("Введите id или имя издателя: ")
    find_info_by_publisher(session, publisher)