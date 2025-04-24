from sqlalchemy import Column, Integer, String, Float, Text
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<Product(title={self.title}, price={self.price})>"
