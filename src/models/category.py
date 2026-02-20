import uuid
from sqlalchemy import Column, String, Text, Uuid
from sqlalchemy.orm import relationship
from src.db.database import Base
from .product_categories import product_categories

class Category(Base):
    __tablename__ = "categories"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    
    products = relationship("Product", secondary=product_categories, back_populates="categories")
