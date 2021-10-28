from fastapi import FastAPI

from app.core.settings import settings
from app.node.node import node_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
    debug=True,
)

app.include_router(node_router)

if __name__ == '__main__':
    from uvicorn import run

    run(app=app, host='0.0.0.0', port=8000, log_level='info')
