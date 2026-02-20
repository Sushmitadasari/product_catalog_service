from typing import List, Optional
from src.domain.uow import IUnitOfWork
from src.schemas.product import ProductCreate, ProductUpdate
from src.models.product import Product

class ProductService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        with self.uow as uow:
            return uow.products.get_all(skip, limit)

    def get_by_id(self, item_id: str) -> Optional[Product]:
        with self.uow as uow:
            return uow.products.get_by_id(item_id)

    def search(self, q: Optional[str] = None, category_id: Optional[str] = None, 
               min_price: Optional[float] = None, max_price: Optional[float] = None, 
               skip: int = 0, limit: int = 100) -> List[Product]:
        with self.uow as uow:
            return uow.products.search(q, category_id, min_price, max_price, skip, limit)

    def create(self, item: ProductCreate) -> Product:
        with self.uow as uow:
            data = item.model_dump(exclude={"category_ids"})
            db_item = Product(**data)

            if item.category_ids:
                for cat_id in item.category_ids:
                    cat = uow.categories.get_by_id(str(cat_id))
                    if cat:
                        db_item.categories.append(cat)

            created = uow.products.add(db_item)
            uow.commit()
            return created

    def update(self, item_id: str, item: ProductUpdate) -> Optional[Product]:
        with self.uow as uow:
            db_item = uow.products.get_by_id(item_id)
            if not db_item:
                return None
            
            update_data = item.model_dump(exclude_unset=True, exclude={"category_ids"})
            for key, value in update_data.items():
                setattr(db_item, key, value)

            if item.category_ids is not None:
                db_item.categories.clear()
                for cat_id in item.category_ids:
                    cat = uow.categories.get_by_id(str(cat_id))
                    if cat:
                        db_item.categories.append(cat)
            
            uow.commit()
            return db_item

    def delete(self, item_id: str) -> bool:
        with self.uow as uow:
            deleted = uow.products.delete(item_id)
            if deleted:
                uow.commit()
            return deleted
