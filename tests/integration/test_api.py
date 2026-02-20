import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.database import Base
from src.api.dependencies import get_uow
from src.uow.sql_uow import SQLUnitOfWork

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_uow():
    return SQLUnitOfWork(session_factory=TestingSessionLocal)

app.dependency_overrides[get_uow] = override_get_uow

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_category():
    response = client.post("/categories", json={"name": "Test Category", "description": "integration test"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"
    assert "id" in data

def test_create_product():
    cat_resp = client.post("/categories", json={"name": "Electronics"})
    cat_id = cat_resp.json()["id"]

    response = client.post("/products", json={
        "name": "Integration Phone",
        "description": "A phone for testing",
        "price": 500.0,
        "sku": "INT-PH-1",
        "category_ids": [cat_id]
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Integration Phone"
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == cat_id

def test_search_product():
    client.post("/products", json={"name": "Gaming Mouse", "description": "High DPI", "price": 49.99, "sku": "GM-01"})
    client.post("/products", json={"name": "Office Mouse", "description": "Ergonomic basic", "price": 19.99, "sku": "OM-01"})
    
    response = client.get("/products/search?q=Gaming")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Gaming Mouse"
    
    response_price = client.get("/products/search?max_price=30")
    assert response_price.status_code == 200
    data_price = response_price.json()
    assert len(data_price) == 1
    assert data_price[0]["name"] == "Office Mouse"
