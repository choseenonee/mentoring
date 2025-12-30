from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Product
from app.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: ProductCreate) -> Product:
        product = Product(
            name=payload.name,
            price=payload.price,
            in_stock=payload.in_stock,
        )

        self.session.add(product)

        await self.session.commit()
        await self.session.refresh(product)

        return product

    async def get_list(self, *, q: str | None, limit: int, offset: int) -> Sequence[Product]:
        stmt = select(Product).order_by(Product.id).limit(limit).offset(offset)
        if q:
            stmt = stmt.where(Product.name.ilike(f"%{q}%"))

        res = await self.session.execute(stmt)

        return res.scalars().all()

    async def get(self, product_id: int) -> Product | None:
        res = await self.session.execute(select(Product).where(Product.id == product_id))

        return res.scalar_one_or_none()

    async def replace(self, product_id: int, payload: ProductCreate) -> Product | None:
        product = await self.get(product_id)
        if not product:
            return None

        product.name = payload.name
        product.price = payload.price
        product.in_stock = payload.in_stock

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id: int, payload: ProductUpdate) -> Product | None:
        product = await self.get(product_id)
        if not product:
            return None

        if payload.name is not None:
            product.name = payload.name
        if payload.price is not None:
            product.price = payload.price
        if payload.in_stock is not None:
            product.in_stock = payload.in_stock

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get(product_id)
        if not product:
            return False

        await self.session.delete(product)
        await self.session.commit()

        return True
