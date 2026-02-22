from src.db.database import SessionLocal
from src.models.category import Category
from src.schemas.category import CategoryCreate
from src.services.category_service import CategoryService
from src.uow.sql_uow import SQLUnitOfWork
import traceback

print("Testing category creation...")
try:
    uow = SQLUnitOfWork()
    service = CategoryService(uow)
    cat_in = CategoryCreate(name="TestCat", description="Test Description")
    res = service.create(cat_in)
    print("Success:", res.id)
except Exception as e:
    print("Failed to create category")
    traceback.print_exc()
