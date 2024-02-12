import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import json
from models import create_tables, Publisher, Shop, Book, Stock, Sale
from datetime import datetime
from dateutil.parser import parse

import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')

DSN = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}"

def start():
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)       
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    def get_query(id_publisher):
        name = session.query(Publisher.name).filter(Publisher.id == id_publisher).one()
        print("Имя автора: ", name[0])
        print("Продажа книг:")
        subq = session.query(Stock).join(Book.stock).filter(Book.id_publisher == id_publisher).subquery()
        result = session.query(Sale).join(subq, Sale.id_stock == subq.c.id).all()
        if len(result) > 0:
            for c in result:
                print(f"{c.stock.book.title} | {c.stock.shop.name} | {c.price} | {c.date_sale.strftime('%d-%m-%Y')}")
        else:
            print('нет данных')

    txt = input("Введите id или имя автора: ")
    try:
        id_publisher = int(txt)
    except:
        is_exists = session.query(exists().where(Publisher.name.like(f'%{txt}%'))).scalar()
        if is_exists:
            id_author = session.query(Publisher.id).filter(Publisher.name.like(f'%{txt}%')).one()
            get_query(id_author[0])
        else:
            print("Нет автора с таким именем")
    else:
        is_exists = session.query(exists().where(Publisher.id == id_publisher)).scalar()
        if is_exists:
            get_query(id_publisher)
        else:
            print('Нет автора с таким id')
        

    session.close()

if __name__ == "__main__":
    start()
