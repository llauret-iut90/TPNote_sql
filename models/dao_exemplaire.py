
from connexion_db import get_db
from flask import *

def find_details_oeuvre_exemplaires(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution_iso
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
        WHERE oeuvre.id_oeuvre=%s
        GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
        ORDER BY auteur.nom, oeuvre.titre; '''
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_1')

def find_exemplaires_oeuvre(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT exemplaire.id_exemplaire,
       exemplaire.date_achat,
       exemplaire.etat,
       exemplaire.oeuvre_id,
       exemplaire.id_exemplaire,
       oeuvre.date_parution,
       exemplaire.prix,
       COUNT(E1.id_exemplaire)                        AS ExemplaireDispo,
       IF(E1.id_exemplaire IS NULL, 'abs', 'present') AS present
FROM exemplaire
         LEFT JOIN emprunt ON exemplaire.id_exemplaire = emprunt.exemplaire_id
         INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
         LEFT JOIN exemplaire AS E1 ON E1.id_exemplaire = exemplaire.id_exemplaire
    AND E1.id_exemplaire
                                           NOT IN
        (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
WHERE exemplaire.oeuvre_id = %s
GROUP BY exemplaire.id_exemplaire, exemplaire.date_achat, exemplaire.etat, exemplaire.oeuvre_id,
         exemplaire.id_exemplaire, oeuvre.date_parution, exemplaire.prix; '''
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 4_2')

def find_exemplaire_nbEmprunts(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT COUNT(emprunt.exemplaire_id) AS nb_emprunts FROM emprunt WHERE emprunt.exemplaire_id=%s '''
        cursor.execute(sql, (id))
        res_nb_emprunts = cursor.fetchone()
        if 'nb_emprunts' in res_nb_emprunts.keys():
            nb_emprunts=res_nb_emprunts['nb_emprunts']
            return nb_emprunts
    except ValueError:
        abort(400,'erreur requete 4_7')

def find_edit_one_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT * FROM exemplaire WHERE id_exemplaire=%s '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_11')

def find_id_oeuvre_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT oeuvre_id FROM exemplaire WHERE id_exemplaire=%s '''
        cursor.execute(sql, (id))
        oeuvre = cursor.fetchone()
        oeuvre_id=str(oeuvre['oeuvre_id'])
        return oeuvre_id
    except ValueError:
        abort(400,'erreur requete 4_9')

def find_add_exemplaire_info_oeuvre(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre
        FROM oeuvre
        JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
        LEFT JOIN exemplaire AS E1 ON E1.oeuvre_id = oeuvre.id_oeuvre
        WHERE oeuvre.id_oeuvre=%s
        GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
        ORDER BY auteur.nom, oeuvre.titre; '''
        cursor.execute(sql, (id))
        oeuvre = cursor.fetchone()
        return oeuvre
    except ValueError:
        abort(400,'erreur requete 4_3')

def find_edit_details_oeuvre_id_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT id_exemplaire, oeuvre_id, etat, date_achat, prix, auteur.nom, oeuvre.titre 
    FROM exemplaire
    INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
    INNER JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
    WHERE id_exemplaire=%s '''
        cursor.execute(sql, (id))
        exemplaire = cursor.fetchone()
        return exemplaire
    except ValueError:
        abort(400,'erreur requete 4_10')


def exemplaire_insert(titre,dateParution,photo,idAuteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' INSERT INTO exemplaire (oeuvre_id, etat, date_achat, prix) VALUES (%s, %s, %s, %s) '''
        cursor.execute(sql, (titre,dateParution,photo,idAuteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_5')

def exemplaire_update(noOeuvre, etat, dateAchat, prix, id_exemplaire):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' UPDATE exemplaire SET oeuvre_id=%s, etat=%s, date_achat=%s, prix=%s WHERE id_exemplaire=%s '''
        cursor.execute(sql, (noOeuvre, etat, dateAchat, prix, id_exemplaire))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_12')

def exemplaire_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' DELETE FROM exemplaire WHERE id_exemplaire=%s '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_8')
