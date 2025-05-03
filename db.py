import sqlite3
from datetime import datetime

# Connexion à la base de données (création de la base de données mun.db si elle n'existe pas)
conn = sqlite3.connect('fatoubr.db')
cursor = conn.cursor()

# Création de la table 'ventes'
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT NOT NULL,
    total REAL NOT NULL,
    date TEXT NOT NULL
);
''')

# Création de la table 'stocks'
cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produit TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    prix REAL NOT NULL
);
''')

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()

print("Base de données 'fatoubr.db' et tables 'ventes' et 'stocks' créées avec succès.")


