import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import routers_v1
from core.config import settings

# Main app
app = FastAPI()

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Routing
for router in routers_v1:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=True,
    )
