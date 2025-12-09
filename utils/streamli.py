import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["supermarche_db"]
collection = db["ventes"]

st.title(" Ajout de données – Entrepôt Supermarché")

st.write("""
Cette interface permet d'ajouter des ventes dans MongoDB :
- Ajouter une ligne manuellement
""")

def verifier_ligne(data):
    erreurs = []

    champs_obligatoires = ["Item Name_x", "Category Name"]
    for champ in champs_obligatoires:
        if not data.get(champ):
            erreurs.append(f"Le champ '{champ}' est obligatoire.")

    # Vérification quantité
    try:
        if float(data["Quantity Sold (kilo)"]) <= 0:
            erreurs.append("La quantité doit être > 0.")
    except:
        erreurs.append("Quantité invalide.")

    # Vérification prix
    try:
        if float(data["Unit Selling Price (RMB/kg)"]) <= 0:
            erreurs.append("Le prix doit être > 0.")
    except:
        erreurs.append("Prix invalide.")

    return erreurs

# ------------------ AJOUT MANUEL ----------------------------

st.header("Ajouter une vente manuellement")

with st.form("formulaire"):
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", datetime.today())
        time = st.text_input("Heure (HH:MM:SS)", "00:00:00")
        item_name = st.text_input("Nom du produit (Item Name_x)")
        category = st.text_input("Catégorie (Category Name)")

    with col2:
        qty = st.number_input("Quantité vendue (kilo)", min_value=0.01, format="%.2f")
        price = st.number_input("Prix unitaire (RMB/kg)", min_value=0.01, format="%.2f")
        loss = st.number_input("Taux de perte (%)", min_value=0.0, max_value=100.0, value=0.0)

    submitted = st.form_submit_button("Insérer")

    if submitted:
        ligne = {
            "Date": str(date),
            "Time": time,
            "Item Name_x": item_name,
            "Category Name": category,
            "Quantity Sold (kilo)": qty,
            "Unit Selling Price (RMB/kg)": price,
            "Loss Rate (%)": loss,
            "Revenue": round(qty * price, 2)
        }

        erreurs = verifier_ligne(ligne)

        if erreurs:
            st.error("Erreurs trouvées :")
            for e in erreurs:
                st.write(f"- {e}")
        else:
            collection.insert_one(ligne)
            st.success(" Vente ajoutée avec succès !")
            st.json(ligne)

