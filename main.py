from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import (
    users_router,
    drivers_router,
    link_router,
    vehicles_router,
    locations_router,
)

from core.config import settings
from db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.USE_ALEMBIC:
        SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users_router, prefix='/api/v1/users', tags=['Users'])
app.include_router(drivers_router, prefix='/api/v1/drivers', tags=['Drivers'])
app.include_router(vehicles_router, prefix='/api/v1/vehicles', tags=['Vehicles'])
app.include_router(locations_router, prefix='/api/v1/locations', tags=['Known locations'])
app.include_router(link_router, prefix='/api/v1/link_bot', tags=['Link Telegram Bot'])

@app.get('/health', tags=['Health'])
def health_check() -> dict[str, str]:
    return {'status': 'healthy'}
