import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Products API",
    description="CRUD API for managing products",
    version="1.0.0",
)

db: dict = {}


class ProductInput(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    category: str


class Product(ProductInput):
    id: str
    createdAt: datetime
    updatedAt: datetime


@app.get("/products", response_model=list[Product])
def list_products():
    return list(db.values())


@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductInput):
    product = Product(
        id=str(uuid.uuid4()),
        createdAt=datetime.now(tz=timezone.utc),
        updatedAt=datetime.now(tz=timezone.utc),
        **payload.model_dump(),
    )
    db[product.id] = product
    return product


@app.get("/products/{id}", response_model=Product)
def get_product(id: str):
    if id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    return db[id]


@app.put("/products/{id}", response_model=Product)
def update_product(id: str, payload: ProductInput):
    if id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = Product(
        id=id,
        createdAt=db[id].createdAt,
        updatedAt=datetime.now(tz=timezone.utc),
        **payload.model_dump(),
    )
    db[id] = updated
    return updated


@app.delete("/products/{id}", status_code=204)
def delete_product(id: str):
    if id not in db:
        raise HTTPException(status_code=404, detail="Product not found")
    del db[id]
