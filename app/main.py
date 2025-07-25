from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import user as user_router
from app.api.v1 import category as category_router
from app.api.v1 import transaction as transaction_router
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    print(f"Request body: {body.decode()}")

    # "восстанавливаем" тело запроса для дальнейшей обработки
    async def receive():
        return {"type": "http.request", "body": body}

    response = await call_next(Request(request.scope, receive))
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router.router, prefix="/api/v1/user")
app.include_router(category_router.router, prefix="/api/v1/category")
app.include_router(transaction_router.router, prefix="/api/v1/transaction")

@app.get("/")
def read_root():
    return {"message" : "finance traker api is running "}

# Обработка стандартных HTTP ошибок
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Обработка ошибок БД (например, нарушение уникальности)
@app.exception_handler(IntegrityError)
async def db_integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Database Integrity Error", "error": str(exc.orig)}
    )

# Обработка всех остальных неожиданных ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Unexpected Error Occurred", "error": str(exc)}
    )