import os
import json
from fastapi import FastAPI
from mistralai.client import MistralClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
app = FastAPI()

# Récupérer la clé API
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("La clé API MISTRAL n'est pas définie. Vérifie ton fichier .env.")

# Initialiser le client Mistral
client = MistralClient(api_key=api_key)

# Exemple de menu du jour
menu_du_jour = {
    "entrées": {"Soupe du jour": 5, "Salade de chèvre chaud": 7},
    "plats principaux": {"Filet de saumon, riz sauvage": 15, "Poulet rôti, pommes de terre": 14, "Lasagnes maison": 12},
    "desserts": {"Mousse au chocolat": 6, "Tarte aux pommes": 5}
}

def afficher_menu():
    """Affiche le menu au format JSON."""
    return menu_du_jour

@app.get("/")
def lire_menu():
    """Route API pour afficher le menu."""
    return {"menu": afficher_menu()}

@app.post("/commande/")
def traiter_commande(commande: dict):
    """Traite une commande en appelant Mistral AI."""
    message = commande.get("message", "")
    if not message:
        return {"erreur": "Aucune commande reçue"}

    # Envoyer la commande à Mistral AI
    messages = [{"role": "user", "content": message}]
    response = client.chat(model="mistral-large", messages=messages)
    
    return {"reponse": response.choices[0].message.content}
