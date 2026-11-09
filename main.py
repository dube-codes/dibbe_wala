from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables


from routes.orders import router as orders_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_tables()
    print("Database tables created successfully.")
    yield
    print("Application shutdown complete.")


ver = "v1"
app = FastAPI(
    title="Dabbewala Delivery API",
    description="API for managing dabbewala deliveries and tracking order statuses.!",
    version=ver,
    lifespan=lifespan,
)


@app.get("/")
def index():
    return {"message": f"Welcome to the Dabbewala Delivery API version : {ver}"}


app.include_router(orders_router, prefix=f"/api/{ver}/orders", tags=["Orders"])
app.include_router(stats_router, prefix=f"/api/{ver}/stats", tags=["Stats"])
