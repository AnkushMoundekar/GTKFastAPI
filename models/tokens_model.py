from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey
from database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(BigInteger, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("Auth_users.id"))
    token = Column(String, unique= True, index=True)