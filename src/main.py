from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.dependencies import get_api_key
from src.activities import router as activities_router
from src.buildings import router as buildings_router
from src.organizations import router as organizations_router


app = FastAPI(
    title="Organizations API",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    dependencies=[Depends(get_api_key)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    organizations_router, prefix="/organizations", tags=["Organizations"]
)
app.include_router(buildings_router, prefix="/buildings", tags=["Buildings"])
app.include_router(activities_router, prefix="/activities", tags=["Activities"])


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "message": "Organizations API is running"}
