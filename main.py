import sys
import asyncio

from dotenv import load_dotenv

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

import os
from fastapi import FastAPI
from api import register_routes, register_middlewares, configure
import uvicorn

print("Cargando variables de entorno...")
print(f"ENV: {os.getenv('ENV')}")
if os.getenv("ENV") != "production":
    load_dotenv()

app = FastAPI(
    root_path=os.getenv("endpoint")
)

configure(app)
