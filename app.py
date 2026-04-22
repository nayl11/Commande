import streamlit as st
import requests

st.title("Chatbot de Commande de Restaurant")

# Ajouter plusieurs commandes
st.header("Ajouter des commandes")
user_input = st.text_input("Que souhaitez-vous commander ? (ex: pizza, eau et glace)")
if st.button("Ajouter les commandes"):
    if user_input:
        response = requests.post("http://localhost:8000/orders/", json={"item": user_input})
        if response.status_code == 200:
            st.success("Commandes ajoutées avec succès !")
        else:
            st.error("Erreur lors de l'ajout des commandes.")
    else:
        st.warning("Veuillez entrer au moins une commande.")

# Afficher les commandes en cours
st.header("Commandes en cours")
response = requests.get("http://localhost:8000/orders/")
if response.status_code == 200:
    orders = response.json()
    if orders:
        for order in orders:
            st.write(f"ID: {order['id']} - Item: {order['item']}")
            if st.button("Supprimer", key=order['id']):
                delete_response = requests.delete(f"http://localhost:8000/orders/{order['id']}")
                if delete_response.status_code == 200:
                    st.success("Commande supprimée.")
                else:
                    st.error("Erreur lors de la suppression de la commande.")
    else:
        st.info("Aucune commande en cours.")
else:
    st.error("Erreur lors de la récupération des commandes.")
