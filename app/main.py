from fastapi import FastAPI
from app.api.products import router as products_router

app = FastAPI(title="In-memory CRUD Products")

app.include_router(products_router, prefix="/products", tags=["products"])


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
