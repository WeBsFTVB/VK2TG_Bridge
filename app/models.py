from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AuthKeys(Base):
    __tablename__ = 'auth_keys'
    id = Column(Integer, primary_key=True)
    vk_group_id = Column(String, nullable=False)
    vk_token = Column(String, nullable=False)
    telegram_bot_token = Column(String, nullable=False)
    telegram_chat_id = Column(String, nullable=False)
