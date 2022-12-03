import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.base_logger import logger
from config.config import settings
from api.MU import router as mu_router
from api.MUC import router as muc_router


tags_metadata = [
    {
        "name": "GetMUs",
        "description": "Get all created Smart Devices **MU**s.",
    },
    {
        "name": "CreateMU",
        "description": "Create and Register a new **MU** device to **RA**.",
    },
    {
        "name": "LoadMU",
        "description": "Load saved **MU** object.",
    },
    {
        "name": "login",
        "description": "Login Mobile User **MU** to Mobile Device",
    },
    {
        "name": "logout",
        "description": "Logout connect Mobile User",
    },
    {
        "name": "auth",
        "description": "Authenticate **MU** to given **SD** device.",
    },
    {
        "name": "update_password",
        "description": "Password update for **MU** on the Mobile Device"
    },
    {
        "name": "health",
        "description": "Health Check."
    },
]

app = FastAPI(openapi_tags=tags_metadata)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mu_router, prefix="/MU")
app.include_router(muc_router, prefix="/app/v1")

@app.get("/health", tags=["health"])
def Health():
    return {"OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.MU_API_PORT)
