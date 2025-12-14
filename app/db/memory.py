from typing import Dict, List, Optional
from uuid import uuid4

from app.schemas import ProductCreate, ProductUpdate, ProductOut


_db: Dict[str, ProductOut] = {}


def create_product(payload: ProductCreate) -> ProductOut:
    product_id = str(uuid4())
    product = ProductOut(id=product_id, **payload.model_dump())

    _db[product_id] = product

    return product


def list_products(q: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[ProductOut]:
    items = list(_db.values())

    if q:
        q_lower = q.lower()
        items = [p for p in items if q_lower in p.name.lower()]

    return items[offset : offset + limit]


def get_product(product_id: str) -> Optional[ProductOut]:
    return _db.get(product_id)


def replace_product(product_id: str, payload: ProductCreate) -> ProductOut:
    product = ProductOut(id=product_id, **payload.model_dump())
    _db[product_id] = product

    return product


def update_product(product_id: str, payload: ProductUpdate) -> ProductOut:
    current = _db[product_id]

    data = payload.model_dump(exclude_unset=True)

    updated = current.model_copy(update=data)

    _db[product_id] = updated

    return updated


def delete_product(product_id: str) -> None:
    del _db[product_id]


def count_items() -> int:
    return len(_db)
