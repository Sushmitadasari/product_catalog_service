from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from src.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from src.services.product_service import ProductService
from src.api.dependencies import get_uow
from src.domain.uow import IUnitOfWork

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(uow: IUnitOfWork = Depends(get_uow)) -> ProductService:
    return ProductService(uow)

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create(product)

@router.get("/search", response_model=List[ProductResponse])
def search_products(
    q: Optional[str] = Query(None, description="Search keyword"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    skip: int = 0, limit: int = 100,
    service: ProductService = Depends(get_product_service)
):
    return service.search(q, category_id, min_price, max_price, skip, limit)

@router.get("", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, service: ProductService = Depends(get_product_service)):
    return service.get_all(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, service: ProductService = Depends(get_product_service)):
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate, service: ProductService = Depends(get_product_service)):
    updated = service.update(product_id, product)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, service: ProductService = Depends(get_product_service)):
    deleted = service.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
