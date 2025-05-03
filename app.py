from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
def ajouter_vente(article, total):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('fatoubr.db')
        cursor = conn.cursor()

        # Obtenir la date actuelle au format 'YYYY-MM-DD'
        date_vente = datetime.now().strftime('%Y-%m-%d')

        # Insertion des données dans la table 'ventes'
        cursor.execute('''
            INSERT INTO ventes (article, total, date)
            VALUES (?, ?, ?)
        ''', (article, total, date_vente))

        # Sauvegarder les changements et fermer la connexion
        conn.commit()
        print("Vente ajoutée avec succès !")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la vente : {e}")

    finally:
        # Fermer la connexion
        conn.close()

# Fonction pour obtenir les ventes d'une date donnée
def get_ventes_by_date(date):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('fatoubr.db')
        cursor = conn.cursor()

        # Récupérer les ventes de la date spécifiée
        cursor.execute("SELECT article, total, date FROM ventes WHERE date = ?", (date,))
        ventes = cursor.fetchall()

        # Fermer la connexion
        conn.close()

        # Retourner les résultats
        return ventes

    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des ventes : {e}")
        return []

# Route pour la page "index.html"
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer les données envoyées par le formulaire
    article = request.form['article']
    total = request.form['total']

    # Ajouter la vente dans la base de données
    ajouter_vente(article, total)

    return 'Commande reçue et traitée avec succès !'

@app.route('/afficher_ventes/<date>', methods=['GET'])
def afficher_ventes(date):
    # Récupérer les ventes pour la date spécifiée
    ventes = get_ventes_by_date(date)

    # Renvoyer les résultats en JSON
    if ventes:
        return jsonify([{
            'article': vente[0],
            'total': vente[1],
            'date': vente[2]
        } for vente in ventes])
    else:
        return jsonify([])
    

# Route pour la page "vendre.html"
@app.route('/vendre')
def vendre():
    return render_template('vendre.html')

@app.route('/afficher_ventes')
def afficher_ventes_page():
    return render_template('afficher_vente.html')


@app.route('/stock')
def stock():
    return render_template('stock.html')



def get_db():
    conn = sqlite3.connect('fatoubr.db')
    conn.row_factory = sqlite3.Row
    return conn
# Route pour ajouter un produit au stock
@app.route('/ajouter_stock', methods=['POST'])
def ajouter_stock():
    try:
        data = request.get_json()
        produit = data['produit']
        quantite = data['quantite']
        prix = data['prix']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stocks (produit, quantite, prix)
            VALUES (?, ?, ?)
        ''', (produit, quantite, prix))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Route pour afficher le stock
@app.route('/afficher_stock')
def afficher_stock():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stocks')
    stock = cursor.fetchall()
    conn.close()
    return jsonify({'stock': [dict(row) for row in stock]})

# Route pour déduire la quantité d'un produit
@app.route('/deduire_quantite_stock', methods=['POST'])
def deduire_quantite_stock():
    try:
        data = request.get_json()
        id = data['id']
        quantite = data['quantite']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT quantite FROM stocks WHERE id = ?', (id,))
        result = cursor.fetchone()

        if result and result['quantite'] >= quantite:
            new_quantity = result['quantite'] - quantite
            cursor.execute('UPDATE stocks SET quantite = ? WHERE id = ?', (new_quantity, id))
            conn.commit()
            conn.close()
            return jsonify({'success': True})
        else:
            conn.close()
            return jsonify({'success': False, 'message': "Quantité insuffisante."})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Route pour supprimer un produit
@app.route('/supprimer_stock', methods=['POST'])
def supprimer_stock():
    try:
        data = request.get_json()
        id = data['id']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stocks WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    




if __name__ == '__main__':
    app.run(debug=True)
