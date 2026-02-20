import time
from sqlalchemy.orm import Session
from src.db.database import SessionLocal, engine, Base
from src.models.category import Category
from src.models.product import Product
from decimal import Decimal

def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(Category).count() > 0:
            print("Database already seeded.")
            return

        print("Seeding categories...")
        cat1 = Category(name="Electronics", description="Electronic devices and accessories")
        cat2 = Category(name="Clothing", description="Apparel and fashion")
        cat3 = Category(name="Books", description="Physical and digital books")
        
        db.add_all([cat1, cat2, cat3])
        db.commit()
        
        print("Seeding products...")
        products = [
            Product(name="Smartphone X", description="Latest model smartphone", price=Decimal("799.99"), sku="ELEC-SMART-X", categories=[cat1]),
            Product(name="Laptop Pro", description="High performance laptop", price=Decimal("1299.99"), sku="ELEC-LAPT-PRO", categories=[cat1]),
            Product(name="Wireless Earbuds", description="Noise cancelling earbuds", price=Decimal("149.99"), sku="ELEC-EARB-W", categories=[cat1]),
            Product(name="T-Shirt classic", description="100% Cotton T-Shirt", price=Decimal("19.99"), sku="CLOT-TSHRT-C", categories=[cat2]),
            Product(name="Jeans Regular", description="Blue denim jeans", price=Decimal("49.99"), sku="CLOT-JEAN-R", categories=[cat2]),
            Product(name="Winter Jacket", description="Warm winter jacket", price=Decimal("120.00"), sku="CLOT-JACK-W", categories=[cat2]),
            Product(name="The Great Novel", description="Bestselling fiction book", price=Decimal("15.99"), sku="BOOK-FICT-GN", categories=[cat3]),
            Product(name="Python Programming", description="Learn Python programming", price=Decimal("45.00"), sku="BOOK-TECH-PP", categories=[cat3]),
            Product(name="Database Design", description="Comprehensive guide to databases", price=Decimal("55.00"), sku="BOOK-TECH-DD", categories=[cat3]),
            Product(name="Smart Watch", description="Fitness tracking watch", price=Decimal("199.99"), sku="ELEC-WATCH-S", categories=[cat1]),
        ]
        db.add_all(products)
        db.commit()
        print("Seeding complete!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
