
from connexion_db import get_db
from flask import *

def find_adherents_emprunter():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_1' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_1')

def find_adherents_rendre():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_2' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_2')

def find_adherent_nbre_emprunt_retardDatePaiment(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_3' FROM DUAL '''
        cursor.execute(sql,(id_adherent))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 5_3')

def find_adherent_data(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_7' FROM DUAL '''
        cursor.execute(sql,(id_adherent))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 5_7')

def find_exemplaire_oeuvre_disponible():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_4' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_4')

def find_emprunt_data_adherent(id_adherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_5' FROM DUAL '''
        cursor.execute(sql, (id_adherent))
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_5')

def find_select_emprunt_split(list_emprunts_split):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_9' FROM DUAL '''
        cursor.execute(sql, list_emprunts_split)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_9')

def find_adherents_dropdown():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_12' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_12')

def find_adherents_select_emprunts(idAdherent):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_11' FROM DUAL '''
        if idAdherent.isnumeric():
            sql = sql + " WHERE adherent.id =" + str(idAdherent)
        sql = sql + " ORDER BY nomAdherent ASC, dateEmprunt DESC "
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
        sql = ''' SELECT 'requete5_13' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 5_13')


def emprunt_insert(idAdherent,noExemplaire,dateEmprunt):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_6' FROM DUAL '''
        cursor.execute(sql, (idAdherent,noExemplaire,dateEmprunt))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_6')

def emprunt_update(dateRetour, idAdherent,dateEmprunt,noExemplaire):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_8' FROM DUAL '''
        cursor.execute(sql, (dateRetour, idAdherent,dateEmprunt,noExemplaire))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_8')

def emprunt_delete(list_emprunts_split):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete5_10' FROM DUAL '''
        cursor.execute(sql, list_emprunts_split)
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 5_8')