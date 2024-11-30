from fastapi import FastAPI
import uvicorn
from app.database import check_connection  # Import db from app.database
from app.routes import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_connection()
    yield
    pass

app = FastAPI(lifespan=lifespan)

# Include the router for student-related routes
app.include_router(
    router,
    prefix="/api",
)


if __name__ == "__main__":
    # Run the app with Uvicorn directly when the script is executed
    uvicorn.run(app, host="127.0.0.1", port=8000, )
