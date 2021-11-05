import uvicorn

from app.models.database import database
from app.producer import producer
from app.routers import users
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    await producer.start()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await producer.stop()


app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
