from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.utils.startup import wait_for_database, create_tables_if_not_exist, check_database_health


# This is to load the database with the required tables if they do not exist
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running startup task...")
    await wait_for_database()
    await create_tables_if_not_exist()
    await check_database_health()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Organization Management API",
    lifespan=lifespan
)

#Adding CORS Middleware just as a template
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Organization Management API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
