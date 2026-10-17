from fastapi import FastAPI

from Users.users_api import user_router
from products.products_api import products_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(products_router,tags=["products"])
app.include_router(user_router,tags=["users"])
# CORS configuration
origins = [
    "http://localhost:4200",  # Angular
    "http://localhost:3000",  # React
    "http://localhost:5173",  # Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
