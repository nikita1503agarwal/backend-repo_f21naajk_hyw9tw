from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from schemas import Product, Subscriber, Message
from database import db, create_document, get_documents

app = FastAPI(title="Rockwave Fashions API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test_connection():
    # Simple check route; database module handles actual connection setup
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/products", response_model=List[Product])
async def list_products(category: Optional[str] = None, limit: int = 20):
    filt = {"category": category} if category else {}
    docs = await get_documents("product", filt, limit)
    # Map docs to Product by selecting expected fields
    items: List[Product] = []
    for d in docs:
        try:
            items.append(Product(**{k: d.get(k) for k in Product.model_fields}))
        except Exception:
            continue
    return items


@app.post("/products", response_model=Product)
async def create_product(product: Product):
    doc = await create_document("product", product.model_dump())
    return Product(**{k: doc.get(k) for k in Product.model_fields})


@app.post("/subscribe")
async def subscribe(sub: Subscriber):
    await create_document("subscriber", sub.model_dump())
    return {"message": "Thanks for joining Rockwave!"}


@app.post("/contact")
async def contact(msg: Message):
    await create_document("message", msg.model_dump())
    return {"message": "Thanks for reaching out. We'll get back to you soon."}
