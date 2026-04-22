from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import re

# Configuration de la base de données SQLite
DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modèle de commande pour la base de données
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Modèle de requête pour FastAPI
class OrderRequest(BaseModel):
    item: str

app = FastAPI()

# Fonction pour découper la phrase en plusieurs commandes
def split_orders(prompt: str):
    # Séparation des commandes par virgule ou par "et"
    items = re.split(r",| et ", prompt)
    # Nettoyage des espaces
    return [item.strip() for item in items if item.strip()]

# Route pour ajouter plusieurs commandes
@app.post("/orders/")
def add_orders(order: OrderRequest):
    db = SessionLocal()
    items = split_orders(order.item)
    saved_orders = []

    for item in items:
        new_order = Order(item=item)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        saved_orders.append({"id": new_order.id, "item": new_order.item})

    db.close()
    return {"orders": saved_orders}

# Route pour récupérer les commandes en cours
@app.get("/orders/")
def get_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return [{"id": order.id, "item": order.item} for order in orders]

# Route pour supprimer une commande par ID
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    db.delete(order)
    db.commit()
    db.close()
    return {"message": "Commande supprimée"}
