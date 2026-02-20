from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.domain.uow import IProductRepository
from src.models.product import Product
from src.models.category import Category

class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: str) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.session.query(Product).offset(skip).limit(limit).all()

    def add(self, item: Product) -> Product:
        self.session.add(item)
        return item

    def update(self, item_id: str, item: Product) -> Optional[Product]:
        existing_item = self.get_by_id(item_id)
        if existing_item:
            for key, value in item.__dict__.items():
                if not key.startswith('_') and key not in ['id', 'created_at', 'categories']:
                    setattr(existing_item, key, value)
            return existing_item
        return None

    def delete(self, item_id: str) -> bool:
        item = self.get_by_id(item_id)
        if item:
            self.session.delete(item)
            return True
        return False

    def search(self, q: Optional[str] = None, category_id: Optional[str] = None, 
               min_price: Optional[float] = None, max_price: Optional[float] = None, 
               skip: int = 0, limit: int = 100) -> List[Product]:
        query = self.session.query(Product)

        if q:
            search_filter = or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%")
            )
            query = query.filter(search_filter)

        if category_id:
            query = query.join(Product.categories).filter(Category.id == category_id)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        return query.offset(skip).limit(limit).all()
