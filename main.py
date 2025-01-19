import uvicorn
from fastapi import FastAPI
from routers.user_router import user


def create_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(user)

    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)