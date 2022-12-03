import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import settings
from api.SD import router as sd_router
from services.SD import serve

tags_metadata = [
    {
        "name": "GetSDs",
        "description": "Get all created Smart Devices **SD**s.",
    },
    {
        "name": "CreateSD",
        "description": "Create and Register a new **SD** device to **RA**.",
    },
    {
        "name": "LoadSD",
        "description": "Load saved **SD** object.",

    },
    {
        "name": "DeleteSD",
        "description": "Delete **SD** object.",

    },
    {
        "name": "DeleteSDs",
        "description": "Delete All **SD** objects.",

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

app.include_router(sd_router, prefix="/SD")


@app.get("/health", tags=["health"])
def Health():
    return {"OK"}


async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=settings.SD_API_PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    # Uvicorn API server
    loop.create_task(main())
    # gRPC Server
    loop.create_task(serve())
    loop.run_forever()
