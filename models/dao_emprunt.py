
from connexion_db import get_db
from flask import *

def find_adherents_emprunter():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' 
SELECT ad.id_adherent,ad.nom,ad.date_paiement
FROM adherent ad
LEFT JOIN emprunt em on ad.id_adherent = em.adherent_id
WHERE (ad.date_paiement+INTERVAL 1 YEAR > CURDATE()) AND ad.id_adherent NOT IN (
SELECT DISTINCT em.adherent_id
FROM emprunt em
WHERE DATEDIFF(IFNULL(em.date_retour, CURDATE()), em.date_emprunt) > 90
GROUP BY em.adherent_id
HAVING COUNT(em.adherent_id) < 6
    ) AND ad.id_adherent NOT IN (SELECT adherent_id FROM emprunt 
    WHERE date_retour IS NULL GROUP BY adherent_id HAVING COUNT(adherent_id) >=5)
GROUP BY ad.id_adherent,ad.nom,ad.date_paiement
ORDER BY ad.nom; '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_1')

def find_adherents_rendre():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT DISTINCT ad.nom,ad.id_adherent
FROM emprunt e
LEFT JOIN adherent ad on e.adherent_id = ad.id_adherent
WHERE e.date_retour IS NULL
ORDER BY ad.nom;'''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_2')

def find_adherent_nbre_emprunt_retardDatePaiment(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT COUNT(*) AS nbr_emprunt,
       SUM(CASE WHEN IFNULL(em.date_retour, NOW()) > em.date_emprunt + INTERVAL 90 DAY THEN 1 ELSE 0 END) AS retard
FROM emprunt em
WHERE em.adherent_id = %s AND em.date_retour IS NULL; '''
        cursor.execute(sql,(id_adherent))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 5_3')

def find_adherent_data(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT id_adherent,nom,adresse,date_paiement
FROM adherent
WHERE id_adherent = %s '''
        cursor.execute(sql,(id_adherent))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 5_7')

def find_exemplaire_oeuvre_disponible():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT au.nom,oe.titre,oe.id_oeuvre AS noOeuvre,ex.id_exemplaire AS id_exemplaire
FROM exemplaire ex
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre
LEFT JOIN auteur au ON oe.auteur_id = au.id_auteur
WHERE ex.id_exemplaire NOT IN (
    SELECT exemplaire_id FROM emprunt WHERE date_retour IS NULL
    )
ORDER BY au.nom  '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_4')

def find_emprunt_data_adherent(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = '''  SELECT em.adherent_id AS id_adherent,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(CURDATE(), em.date_emprunt) as nb_jours_emprunt, em.date_emprunt
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON ex.id_exemplaire = em.exemplaire_id
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre
WHERE em.adherent_id = %s AND em.date_retour IS NULL
ORDER BY em.date_emprunt DESC; '''
        cursor.execute(sql, (id_adherent))
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_5')

def find_select_emprunt_split(list_emprunts_split):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT * FROM emprunt WHERE adherent_id = %s AND exemplaire_id = %s AND date_emprunt = %s '''
        cursor.execute(sql, list_emprunts_split)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_9')

def find_adherents_dropdown():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT id_adherent,nom FROM adherent ORDER BY nom;  '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_12')

def find_adherents_select_emprunts(idAdherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT em.adherent_id AS id_adherent,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(IFNULL(em.date_retour, CURDATE()), em.date_emprunt) AS nb_jours_emprunt
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON ex.id_exemplaire = em.exemplaire_id
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre '''
        if idAdherent.isnumeric():
            sql = sql + " WHERE em.adherent_id =" + str(idAdherent)
        sql = sql + " ORDER BY ad.nom ASC, em.date_emprunt DESC "
              #" ORDER BY adherent.nom, emprunt.date_emprunt"
        #        ORDER BY nomAdherent ASC, dateEmprunt DESC
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_11')

def find_bilan_emprunt():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT em.adherent_id,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(CURDATE(), em.date_emprunt) AS nbJoursEmprunt
    , DATEDIFF(CURDATE(), em.date_emprunt+ INTERVAL 90 DAY) AS retard, em.date_emprunt + INTERVAL 90 DAY AS dateRenduTheorique
    , IF(DATEDIFF(CURDATE(), em.date_emprunt) > 90, 1,0) AS flagRetard, IF(DATEDIFF(CURDATE(), em.date_emprunt) > 120, 1,0) AS flag_penalite
    , IF((DATEDIFF(CURDATE(), em.date_emprunt)-120)*0.5 <= 25, (DATEDIFF(CURDATE(), em.date_emprunt)-120)*0.5, 25) AS dette
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON em.exemplaire_id = ex.id_exemplaire
LEFT JOIN oeuvre oe on ex.oeuvre_id = oe.id_oeuvre
WHERE em.date_retour IS NULL
HAVING nbJoursEmprunt > 90
ORDER BY RETARD DESC '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_13')


def emprunt_insert(idAdherent,noExemplaire,dateEmprunt):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' INSERT INTO emprunt(adherent_id, exemplaire_id, date_emprunt)
VALUES (%s,%s,%s) '''
        cursor.execute(sql, (idAdherent,noExemplaire,dateEmprunt))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_6')

def emprunt_update(dateRetour, idAdherent,dateEmprunt,noExemplaire):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' UPDATE emprunt
SET date_retour=%s
WHERE adherent_id=%s AND date_emprunt=%s AND exemplaire_id=%s '''
        cursor.execute(sql, (dateRetour, idAdherent,dateEmprunt,noExemplaire))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_8')

def emprunt_delete(list_emprunts_split):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT * FROM emprunt WHERE adherent_id = %s AND exemplaire_id = %s AND date_emprunt = %s '''
        cursor.execute(sql, list_emprunts_split)
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_10')