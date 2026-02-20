from sqlalchemy import Table, Column, ForeignKey, Uuid
from src.db.database import Base

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Uuid, ForeignKey("products.id"), primary_key=True),
    Column("category_id", Uuid, ForeignKey("categories.id"), primary_key=True),
)
