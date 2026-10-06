from fastapi import FastAPI, Request

from app.database import engine, Base
from app.models.user import User
from app.models.product import Product
import time
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded 
from app.core.limiter import limiter  


from app.routers.users import router as users_router
from app.routers.products import router as products_router
from app.routers.auth import router as auth_router
from app.routers.files import router as files_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="User Product API",
    version="1.0.0",
)



app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()
    print("\n========== REQUEST ==========")
    print("Method      :", request.method)
    print("URL         :", request.url)
    print("Path        :", request.url.path)
    print("Query Params:", request.query_params)
    print("Client IP   :", request.client.host if request.client else None)
    headers = dict(request.headers)
    headers.pop("authorization", None)
    print("Headers     :", headers)
    response = await call_next(request)
    execution_time = time.perf_counter() - start_time
    print("========== RESPONSE ==========")
    print("Status Code :", response.status_code)
    print("Headers     :", dict(response.headers))
    print(f"Execution Time: {execution_time:.4f} seconds")
    print("==============================\n")

    return response


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(files_router)


@app.get("/")
async def home():
    return {
        "message": "Welcome to User Product API"
    }
