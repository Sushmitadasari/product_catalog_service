from fastapi import FastAPI
from src.db.database import Base, engine
from src.api.routes import category_routes, product_routes

# Note: In production we should use Alembic for migrations.
# Calling create_all easily creates our tables on startup for this exercise.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Catalog Service",
    description="E-commerce Product Catalog Management API",
    version="1.0.0"
)

app.include_router(category_routes.router)
app.include_router(product_routes.router)

@app.get("/health")
def health_check():
    return {"status": "UP"}
