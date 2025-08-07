import uvicorn
from fastapi import FastAPI

from app.manage import configure_app
from app.utils.constant import APP_NAME , APP_DESCRIPTION , APP_VERSION


def intialize_app() -> FastAPI:

    fastapi_app = FastAPI(title=APP_NAME,
            version=APP_VERSION,
            description=APP_DESCRIPTION)
    
    configure_app(fastapi_app)
    return fastapi_app


server = intialize_app()


if __name__ == "__main__":
    uvicorn.run("app.main:server" , host="0.0.0.0" , port=8000 , reload=True)