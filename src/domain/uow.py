from abc import ABC, abstractmethod
from src.domain.repository import IRepository
from src.models.product import Product
from src.models.category import Category
from typing import List, Optional

class IProductRepository(IRepository[Product]):
    @abstractmethod
    def search(self, q: Optional[str] = None, category_id: Optional[str] = None, 
               min_price: Optional[float] = None, max_price: Optional[float] = None, 
               skip: int = 0, limit: int = 100) -> List[Product]:
        pass

class ICategoryRepository(IRepository[Category]):
    pass

class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def products(self) -> IProductRepository:
        pass

    @property
    @abstractmethod
    def categories(self) -> ICategoryRepository:
        pass

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def dispose(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
