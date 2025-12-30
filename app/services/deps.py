from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_session
from app.services.products import ProductService


def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(session)
