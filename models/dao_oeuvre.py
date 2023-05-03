
from connexion_db import get_db
from flask import *

def find_oeuvres():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = '''  SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution_iso
        , COALESCE (oeuvre.photo, '') AS photo
        , COUNT(E1.id_exemplaire) AS nb_exemplaire
        , COUNT(E2.id_exemplaire) AS nb_exemp_dispo
        , CONCAT(LPAD(CAST(DAY(oeuvre.date_parution)AS CHAR(2)),2,0),'/',LPAD(MONTH(oeuvre.date_parution), 2, '0'),'/', YEAR(oeuvre.date_parution)) 
        AS date_parution
        FROM oeuvre
        JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
        LEFT JOIN exemplaire AS E1 ON E1.oeuvre_id = oeuvre.id_oeuvre
        LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = E1.id_exemplaire
        AND E2.id_exemplaire
        NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
        GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
        ORDER BY auteur.nom ASC, oeuvre.titre ASC; '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 3_1')

def find_oeuvre_nbExemplaires(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT COUNT(exemplaire.id_exemplaire) AS nb_exemplaires 
    FROM oeuvre 
    INNER JOIN exemplaire ON oeuvre.id_oeuvre = exemplaire.oeuvre_id 
    WHERE oeuvre.id_oeuvre = %s '''
        cursor.execute(sql, (id))
        res_nb_exemplaires = cursor.fetchone()
        if 'nb_exemplaires' in res_nb_exemplaires.keys():
            nb_exemplaires=res_nb_exemplaires['nb_exemplaires']
            return nb_exemplaires
    except ValueError:
        abort(400,'erreur requete 3_7')

def find_one_oeuvre(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = '''  SELECT oeuvre.id_oeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, oeuvre.auteur_id, auteur.nom 
    FROM oeuvre 
    INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur 
    WHERE oeuvre.id_oeuvre = %s '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 3_4')


def oeuvre_insert(titre,dateParution,photo,idAuteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' INSERT INTO oeuvre (titre, date_parution, photo, auteur_id) VALUES (%s,%s,%s,%s) '''
        cursor.execute(sql, (titre,dateParution,photo,idAuteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_2')

def oeuvre_update(titre,idAuteur,dateParution,photo,id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' UPDATE oeuvre SET titre=%s, auteur_id=%s, date_parution=%s, photo=%s WHERE id_oeuvre=%s '''
        cursor.execute(sql, (titre,idAuteur,dateParution,photo,id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_5')

def oeuvre_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' DELETE FROM oeuvre WHERE id_oeuvre = %s '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_3')
