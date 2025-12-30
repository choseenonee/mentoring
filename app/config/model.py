from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    host: str = Field()
    port: int = Field()
    user: str = Field()
    password: str = Field()
    database: str = Field()

    timeout: int = Field(default=30, description="Timeout in second at the database connection level")


class AppConfig(BaseModel):
    postgres: PostgresConfig = Field()
