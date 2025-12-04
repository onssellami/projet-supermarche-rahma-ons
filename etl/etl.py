# src/etl.py - Fait par Ons & Rahma - Version finale fonctionnelle
import pandas as pd
from pymongo import MongoClient

print("Démarrage de l'ETL - Fusion des 4 annexes")

# Charger les fichiers
annex1 = pd.read_csv("data/annex1.csv")
annex2 = pd.read_csv("data/annex2.csv")
annex3 = pd.read_csv("data/annex3.csv")
annex4 = pd.read_csv("data/annex4.csv")

print("Annexes chargées !")

# Fusions
data = pd.merge(annex2, annex1, on="Item Code", how="left")
data = pd.merge(data, annex4, on="Item Code", how="left")
data = pd.merge(data, annex3, on=["Item Code", "Date"], how="left")

print(f"Total après fusion : {len(data)} ventes")

# Nettoyage + calculs
data.dropna(subset=["Quantity Sold (kilo)", "Unit Selling Price (RMB/kg)", "Date"], inplace=True)

data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

# CORRECTION ICI : Time → string
data["Time"] = pd.to_datetime(data["Time"], format='%H:%M:%S.%f', errors="coerce").dt.strftime('%H:%M:%S')

# Calcul du CA par ligne
data["Revenue"] = data["Quantity Sold (kilo)"] * data["Unit Selling Price (RMB/kg)"]

print(f"Après nettoyage : {len(data):,} ventes valides")

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["supermarche_db"]
collection = db["ventes"]

collection.delete_many({})  # on repart à zéro
result = collection.insert_many(data.to_dict("records"))

print(f"{len(result.inserted_ids):,} ventes insérées avec succès dans MongoDB !")
