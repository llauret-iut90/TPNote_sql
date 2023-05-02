from connexion_db import get_db
from flask import *


def find_adherents():
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' SELECT COUNT(adherent_id) AS nbr_emprunt, a.nom, a.adresse, a.date_paiement, a.id_adherent,
    DATE_ADD(a.date_paiement, INTERVAL 1 YEAR) AS date_paiement_futur,
    IF(CURRENT_DATE() > DATE_ADD(a.date_paiement, INTERVAL 1 YEAR), 1, 0) AS retard,
    IF(CURRENT_DATE() > DATE_ADD(a.date_paiement, INTERVAL 11 MONTH), 1, 0) AS retardProche
    FROM adherent a
    LEFT JOIN emprunt e on a.id_adherent = e.adherent_id AND e.date_retour IS NULL
    GROUP BY a.nom, a.adresse, a.date_paiement, a.id_adherent
    ORDER BY nom;
    '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400, 'erreur requete 2_1')


def find_adherent_nbEmprunts(id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' SELECT COUNT(emprunt.adherent_id) AS nb_emprunts FROM emprunt WHERE emprunt.adherent_id=%s '''
        cursor.execute(sql, (id))
        res_nb_emprunts = cursor.fetchone()
        if 'nb_emprunts' in res_nb_emprunts.keys():
            nb_emprunts = res_nb_emprunts['nb_emprunts']
            return nb_emprunts
    except ValueError:
        abort(400, 'erreur requete 2_6')


def find_one_adherent(id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' SELECT nom, adresse, date_paiement, id_adherent FROM adherent WHERE id_adherent = %s  '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400, 'erreur requete')


def adherent_insert(nom, adresse, datePaiement):
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' INSERT INTO adherent (nom,adresse,date_paiement) VALUES (%s,%s,%s) '''
        cursor.execute(sql, (nom, adresse, datePaiement))
        connection.commit()
    except ValueError:
        abort(400, 'erreur requete 1_2')


def adherent_update(nom, adresse, datePaiement, id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' UPDATE adherent SET nom=%s,adresse=%s,date_paiement=%s WHERE id_adherent=%s '''
        cursor.execute(sql, (nom, adresse, datePaiement, id))
        connection.commit()
    except ValueError:
        abort(400, 'erreur requete 2_5')


def adherent_delete(id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        sql = ''' DELETE FROM adherent WHERE id_adherent=%s '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400, 'erreur requete 2_3')
