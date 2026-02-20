import pytest
from unittest.mock import Mock, MagicMock
from src.services.product_service import ProductService
from src.schemas.product import ProductCreate
from src.models.product import Product

def test_product_service_create():
    mock_uow = MagicMock()
    mock_products_repo = Mock()
    mock_categories_repo = Mock()
    
    mock_products_repo.add.return_value = Product(id="123", name="Test Product", price=10.0, sku="TEST-123")
    
    mock_uow.products = mock_products_repo
    mock_uow.categories = mock_categories_repo
    mock_uow.__enter__.return_value = mock_uow
    
    service = ProductService(mock_uow)
    product_data = ProductCreate(name="Test Product", price=10.0, sku="TEST-123", category_ids=[])
    
    result = service.create(product_data)
    
    assert result.name == "Test Product"
    mock_products_repo.add.assert_called_once()
    mock_uow.commit.assert_called_once()

def test_product_service_search():
    mock_uow = MagicMock()
    mock_products_repo = Mock()
    
    mock_products_repo.search.return_value = [Product(id="123", name="Search Product", price=10.0, sku="SEARCH-123")]
    
    mock_uow.products = mock_products_repo
    mock_uow.__enter__.return_value = mock_uow
    
    service = ProductService(mock_uow)
    
    result = service.search(q="Search")
    
    assert len(result) == 1
    assert result[0].name == "Search Product"
    mock_products_repo.search.assert_called_once_with("Search", None, None, None, 0, 100)
