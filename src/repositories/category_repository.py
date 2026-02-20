from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.uow import ICategoryRepository
from src.models.category import Category

class CategoryRepository(ICategoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, item_id: str) -> Optional[Category]:
        return self.session.query(Category).filter(Category.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.session.query(Category).offset(skip).limit(limit).all()

    def add(self, item: Category) -> Category:
        self.session.add(item)
        return item

    def update(self, item_id: str, item: Category) -> Optional[Category]:
        existing_item = self.get_by_id(item_id)
        if existing_item:
            for key, value in item.__dict__.items():
                if not key.startswith('_') and key != 'id':
                    setattr(existing_item, key, value)
            return existing_item
        return None

    def delete(self, item_id: str) -> bool:
        item = self.get_by_id(item_id)
        if item:
            self.session.delete(item)
            return True
        return False
