from database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    is_active = Column(Boolean, server_default='TRUE')
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
