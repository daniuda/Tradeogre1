from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import Config

Base = declarative_base()

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(String, primary_key=True)
    exchange = Column(String)
    pair = Column(String)
    price = Column(Float)
    timestamp = Column(DateTime)

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)