from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class ApiKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True)
    vk_api_key = Column(String, nullable=False)
    tg_api_key = Column(String, nullable=False)

Base.metadata.create_all(engine)
