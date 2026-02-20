from typing import List, Optional
from src.domain.uow import IUnitOfWork
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.models.category import Category

class CategoryService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        with self.uow as uow:
            return uow.categories.get_all(skip, limit)

    def get_by_id(self, item_id: str) -> Optional[Category]:
        with self.uow as uow:
            return uow.categories.get_by_id(item_id)

    def create(self, item: CategoryCreate) -> Category:
        with self.uow as uow:
            db_item = Category(**item.model_dump())
            created = uow.categories.add(db_item)
            uow.commit()
            return created

    def update(self, item_id: str, item: CategoryUpdate) -> Optional[Category]:
        with self.uow as uow:
            db_item = uow.categories.get_by_id(item_id)
            if not db_item:
                return None
            
            update_data = item.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_item, key, value)
            
            uow.commit()
            return db_item

    def delete(self, item_id: str) -> bool:
        with self.uow as uow:
            deleted = uow.categories.delete(item_id)
            if deleted:
                uow.commit()
            return deleted
