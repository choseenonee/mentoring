from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

import app.db as db
from app.schemas import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()


@router.post("", response_model=ProductOut, status_code=201)
def create(payload: ProductCreate) -> ProductOut:
    return db.create_product(payload)


@router.get("", response_model=List[ProductOut])
def list(
    q: Optional[str] = Query(default=None, description="Search by name (substring)"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> List[ProductOut]:
    return db.list_products(q=q, limit=limit, offset=offset)


@router.get("/{product_id}", response_model=ProductOut)
def get(product_id: str) -> ProductOut:
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductOut)
def replace(product_id: str, payload: ProductCreate) -> ProductOut:
    if not db.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    return db.replace_product(product_id, payload)


@router.patch("/{product_id}", response_model=ProductOut)
def update(product_id: str, payload: ProductUpdate) -> ProductOut:
    if not db.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    return db.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=204)
def delete(product_id: str) -> None:
    if not db.get_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete_product(product_id)

    return None
