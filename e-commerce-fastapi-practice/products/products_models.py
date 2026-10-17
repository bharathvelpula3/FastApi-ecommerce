from pydantic import ConfigDict, BaseModel
from sqlalchemy import Column, Integer, String, Float
from products.products_database import Base



from sqlalchemy import Column, Integer, String, Float
from .products_database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    category = Column(String)
    image = Column(String)

    # Fields from the nested rating object
    rating_rate = Column(Float)
    rating_count = Column(Integer)

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str | None
    category: str | None
    image: str
    rating_rate: float| None
    rating_count: int | None

    model_config = ConfigDict(from_attributes=True)


