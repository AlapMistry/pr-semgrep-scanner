import os
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from app import app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 4000))
    config = Config()
    config.bind = [f"0.0.0.0:{port}"]
    asyncio.run(serve(app, config))
