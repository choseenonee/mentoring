from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.products import router as products_router
from app.config import load_config
from app.db.connection import make_async_db_url, create_engine, create_session_maker, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_config()
    app.state.config = config

    db_url = make_async_db_url(
        host=config.postgres.host, 
        port=config.postgres.port, 
        user=config.postgres.user, 
        password=config.postgres.password, 
        database=config.postgres.database,
    )
    engine = create_engine(db_url)

    await create_tables(engine)

    session_maker = create_session_maker(engine)

    app.state.engine = engine
    app.state.session_maker = session_maker

    yield

    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="Products API", lifespan=lifespan)

    app.include_router(products_router, prefix="/products", tags=["products"])

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
