import pathlib
from typing import Optional

from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

dotenv_file_path = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"


class Settings(BaseSettings):
    DB_URL: str

    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    SD_H: Optional[str]
    MU_H: Optional[str]
    RA_H: Optional[str]
    HGW_H: Optional[str]

    SD_RPC_PORT: int
    MU_RPC_PORT: int
    RA_RPC_PORT: int
    HGW_RPC_PORT: int

    SD_API_PORT: int
    MU_API_PORT: int
    RA_API_PORT: int
    HGW_API_PORT: int

    # JWT_PUBLIC_KEY: str
    # JWT_PRIVATE_KEY: str
    # REFRESH_TOKEN_EXPIRES_IN: int
    # ACCESS_TOKEN_EXPIRES_IN: int
    # JWT_ALGORITHM: str
    #
    # CLIENT_ORIGIN: str
    class Config:
        env_file: dotenv_file_path


settings = Settings()
