from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CI/CD Learning API", version="1.0.0")


class Item(BaseModel):
    name: str
    price: float


# In-memory "database"
items: dict[int, Item] = {}
next_id = 1


@app.get("/")
def root():
    return {"message": "Hello from my CI/CD pipeline! 🚀"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/items")
def list_items():
    return {"items": items}


@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    items[next_id] = item
    result = {"id": next_id, **item.model_dump()}
    next_id += 1
    return result


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id].model_dump()}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": f"Item {item_id} deleted"}
