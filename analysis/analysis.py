# src/analysis.py - Analyse avec matplotlib + plt.show() - Par Ons & Rahma
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Style propre
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("Connexion à MongoDB et chargement des données...")
client = MongoClient("mongodb://localhost:27017/")
collection = client["supermarche_db"]["ventes"]
df = pd.DataFrame(list(collection.find()))

# Nettoyage rapide
df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
df["Loss Rate (%)"] = pd.to_numeric(df["Loss Rate (%)"], errors="coerce")

# 1. CA Total + Stats clés
ca_total = df["Revenue"].sum()
top_produit = df.groupby("Item Name_x")["Revenue"].sum().idxmax()
ca_top = df.groupby("Item Name_x")["Revenue"].sum().max()

print(f"CA total : {ca_total:,.0f} RMB")
print(f"Produit star : {top_produit} → {ca_top:,.0f} RMB")

# 3. Graphique 2 : Top 10 produits les plus rentables
top10 = df.groupby("Item Name_x")["Revenue"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top10.plot(kind="bar", color="skyblue")
plt.title("Top 10 Produits les Plus Rentables", fontsize=16, fontweight="bold")
plt.xlabel("Produit")
plt.ylabel("CA (RMB)")
plt.xticks(rotation=45, ha="right")
for i, v in enumerate(top10):
    plt.text(i, v + v*0.01, f"{v:,.0f}", ha="center", fontsize=9)
plt.tight_layout()
plt.show()

# 4. Graphique 3 : Taux de perte moyen par catégorie (anomalies)
pertes = df.groupby("Category Name")["Loss Rate (%)"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
pertes.plot(kind="bar", color="salmon")
plt.title("Catégories avec le Plus de Pertes (%)", fontsize=16, fontweight="bold")
plt.xlabel("Catégorie")
plt.ylabel("Taux de perte moyen (%)")
plt.xticks(rotation=45, ha="right")
plt.axhline(y=10, color="red", linestyle="--", label="Seuil critique 10%")
plt.legend()
plt.tight_layout()
plt.show()