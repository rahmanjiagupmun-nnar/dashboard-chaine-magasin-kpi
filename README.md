# 🏪 Dashboard Interactif - Analyse des Ventes

Ce projet est un **dashboard interactif développé avec Dash et Plotly**, permettant d'analyser les ventes d'une chaîne de magasins. Il affiche des **KPIs globaux**, des **graphes interactifs** et permet de filtrer les données par magasin, catégorie et mode de paiement.

---

## 🔹 Fonctionnalités

- **KPI globaux**
  - Total des ventes
  - Nombre de transactions
  - Montant moyen par transaction
  - Satisfaction moyenne des clients

- **Filtres dynamiques**
  - Par magasin
  - Par catégorie de produit
  - Par mode de paiement

- **Graphiques interactifs**
  - Évolution des ventes quotidiennes
  - Répartition des ventes par magasin (Pie Chart)
  - Montant moyen par magasin (Bar Chart)
  - Quantités vendues par catégorie
  - Ventes par catégorie et magasin (Stacked Bar)
  - Modes de paiement les plus utilisés
  - Satisfaction moyenne par magasin
  - Distribution de la satisfaction client

---

## 🔹 Technologies utilisées

- Python 3.x  
- [Dash](https://dash.plotly.com/) pour le framework web  
- [Plotly](https://plotly.com/python/) pour les visualisations interactives  
- [Pandas](https://pandas.pydata.org/) pour la manipulation des données  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) pour le design  
- [NumPy](https://numpy.org/) pour la génération de données simulées  

---

## 🔹 Installation locale

1. **Cloner le dépôt GitHub**
```bash
git clone https://github.com/rahmanjiagupmun-nnar/dashboard-chaine-magasin-kpi.git
cd dashboard-chaine-magasin-kpi

## 
2. Créer un environnement virtuel

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


Installer les dépendances

pip install -r requirements.txt


Lancer le dashboard

python dashs.py


Le dashboard sera accessible à l'adresse http://127.0.0.1:8050
.