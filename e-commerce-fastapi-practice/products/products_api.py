
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated, List

from starlette import status

from .products_database import engine, get_db
from .products_models import Base, Product,ProductResponse

# Create database tables
Base.metadata.create_all(bind=engine)

products_router = APIRouter(
)

# Request body schema
class ProductCreate(BaseModel):
    id: int | None = None
    title: str
    price: float
    description: str
    category: str | None = None
    image: str
    rating_rate: float| None = None
    rating_count: int | None = None

@products_router.post("/products/add-product",status_code=status.HTTP_201_CREATED,response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Annotated[Session, Depends(get_db)]
):
    products = db.query(Product).all()
    # new_product = Product(**product.model_dump(exclude_unset=True))
    max_id= max(product.id for product in products) + 1
    new_product = Product(
        id=max_id,
        title = product.title,
        price = product.price,
        image=product.image,
        description = product.description or "",
        category = product.category or "",
        rating_rate = product.rating_rate if product.rating_rate is not None else 0.0,
        rating_count = product.rating_count if product.rating_count is not None else 0
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@products_router.get("/products",status_code=status.HTTP_200_OK,response_model=List[ProductResponse])
def get_products(
    db: Annotated[Session, Depends(get_db)]
):
    return db.query(Product).all()


@products_router.get("/products/{product_id}",status_code=status.HTTP_200_OK,response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@products_router.delete('/products/delete/{product_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int,db: Annotated[Session, Depends(get_db)]):
    product = db.query(Product).filter(Product.id == product_id).first()
    print(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return None

@products_router.put('/products/update/{product_id}',status_code=status.HTTP_200_OK,response_model=ProductResponse)
def update_product(product_id:int,product:ProductCreate,db: Annotated[Session, Depends(get_db)]):
    update_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if update_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(update_product, key, value)
    db.commit()
    db.refresh(update_product)

    return update_product

@products_router.get('/products/getById/{product_id}',status_code=status.HTTP_200_OK,response_model=ProductResponse)
def getProductById(product_id:int,db: Annotated[Session, Depends(get_db)]):
    get_product = db.query(Product).filter(Product.id == product_id).first()

    if get_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return get_product



