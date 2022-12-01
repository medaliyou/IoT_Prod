import asyncio

import uvicorn
from fastapi import FastAPI
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
        "name": "health",
        "description": "Health Check."
    },
]

app = FastAPI(openapi_tags=tags_metadata)

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
