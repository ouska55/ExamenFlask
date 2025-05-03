import sqlite3
from datetime import datetime

conn = sqlite3.connect('fatoubr.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT NOT NULL,
    total REAL NOT NULL,
    date TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produit TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    prix REAL NOT NULL
);
''')

conn.commit()
conn.close()

print("Base de données 'fatoubr.db' et tables 'ventes' et 'stocks' créées avec succès.")


