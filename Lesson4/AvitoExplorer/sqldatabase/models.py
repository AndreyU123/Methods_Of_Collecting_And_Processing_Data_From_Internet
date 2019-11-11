from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer,
    DECIMAL)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Flats(Base):
    __tablename__='flats'
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String)
    fotos=Column(String)
    price=Column(String)
    announcement_url=Column(String)
    author_url=Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    address=relationship('Addresses', foreign_keys=[address_id])

    def __init__(self,title,fotos,price,announcement_url,author_url,address=None):
        self.title=title
        self.fotos=fotos
        self.price=price
        self.announcement_url=announcement_url
        self.author_url=author_url
        if address:
            self.address=address


class Addresses(Base):
    __tablename__='addresses'
    id=Column(Integer,primary_key=True,autoincrement=True)
    city=Column(String)
    street=Column(String)
    house=Column(String)

    def __init__(self,city,street,house):
        self.city=city
        self.street=street
        self.house=house
