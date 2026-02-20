from sqlalchemy.orm import Session
from src.domain.uow import IUnitOfWork
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository
from src.db.database import SessionLocal

class SQLUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory
        self.session: Session = None

    def begin(self):
        if not self.session:
            self.session = self.session_factory()
        self._products = ProductRepository(self.session)
        self._categories = CategoryRepository(self.session)

    @property
    def products(self):
        return self._products

    @property
    def categories(self):
        return self._categories

    def commit(self):
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()

    def dispose(self):
        if self.session:
            self.session.close()
            self.session = None

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            self.dispose()
