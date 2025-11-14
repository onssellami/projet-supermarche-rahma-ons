
import pandas as pd
from pymongo import MongoClient
import os

print("Début du chargement des ventes")

# Charger le fichier CSV
fichier = "data/supermarket_sales - Sheet1.csv"

if not os.path.exists(fichier):
    print("ERREUR : Le fichier n'est pas là !")
    print("Mets-le dans le dossier data/")
    exit()

data = pd.read_csv(fichier)
print(f"J'ai chargé {len(data)} lignes")
# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
base = client["supermarche_db"]
collection = base["ventes"]
data = data.dropna()  
# Supprime les lignes vides
print("Données nettoyées")
# Vider avant
collection.delete_many({})

# Insérer les données
ventes = data.to_dict("records")
collection.insert_many(ventes)

print(f"{len(ventes)} ventes ajoutées dans MongoDB !")
print("ETL terminé avec succès !")