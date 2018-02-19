"""
Data layer
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Float

Base = declarative_base()


class Price(Base):
    """ Price entity """
    __tablename__ = 'price'
    
    id = Column(Integer, primary_key=True)
    namespace = Column(String)
    symbol = Column(String)
    date = Column(String)
    time = Column(String)
    value = Column(Integer)
    denom = Column(Integer)
    currency = Column(String)

    def __repr__(self):
        return f"<Price ({self.namespace}:{self.symbol},{self.date}:{self.time},{self.value/self.denom}>"
