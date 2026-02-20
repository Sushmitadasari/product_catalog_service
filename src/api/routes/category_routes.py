from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from src.services.category_service import CategoryService
from src.api.dependencies import get_uow
from src.domain.uow import IUnitOfWork

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service(uow: IUnitOfWork = Depends(get_uow)) -> CategoryService:
    return CategoryService(uow)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return service.create(category)

@router.get("", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, service: CategoryService = Depends(get_category_service)):
    return service.get_all(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, service: CategoryService = Depends(get_category_service)):
    category = service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category: CategoryUpdate, service: CategoryService = Depends(get_category_service)):
    updated = service.update(category_id, category)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, service: CategoryService = Depends(get_category_service)):
    deleted = service.delete(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
