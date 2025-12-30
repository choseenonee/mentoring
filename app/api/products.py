from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas import ProductCreate, ProductUpdate, ProductOut
from app.services.deps import get_product_service
from app.services.products import ProductService

router = APIRouter()


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create(
    payload: ProductCreate,
    svc: ProductService = Depends(get_product_service),
) -> ProductOut:
    return await svc.create(payload)


@router.get("", response_model=list[ProductOut])
async def get_list(
    q: str | None = Query(default=None, description="Search by name (substring)"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    svc: ProductService = Depends(get_product_service),
) -> list[ProductOut]:
    products = await svc.get_list(q=q, limit=limit, offset=offset)

    return list(products)


@router.get("/{product_id}", response_model=ProductOut)
async def get(product_id: int,svc: ProductService = Depends(get_product_service)) -> ProductOut:
    product = await svc.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=ProductOut)
async def replace(product_id: int, payload: ProductCreate, svc: ProductService = Depends(get_product_service)) -> ProductOut:
    product = await svc.replace(product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.patch("/{product_id}", response_model=ProductOut)
async def update(product_id: int, payload: ProductUpdate, svc: ProductService = Depends(get_product_service)) -> ProductOut:
    product = await svc.update(product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, svc: ProductService = Depends(get_product_service)) -> None:
    ok = await svc.delete(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")

    return None
