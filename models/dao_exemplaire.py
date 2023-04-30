
from connexion_db import get_db
from flask import *

def find_details_oeuvre_exemplaires(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_1' FROM DUAL '''
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_1')

def find_exemplaires_oeuvre(id_oeuvre):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_2' FROM DUAL '''
        cursor.execute(sql,(id_oeuvre))
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 4_2')

def find_exemplaire_nbEmprunts(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_7' FROM DUAL '''
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
        sql = ''' SELECT 'requete4_11' FROM DUAL '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 4_11')

def find_id_oeuvre_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_9' FROM DUAL '''
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
        sql = ''' SELECT 'requete4_3' FROM DUAL '''
        cursor.execute(sql, (id))
        oeuvre = cursor.fetchone()
        return oeuvre
    except ValueError:
        abort(400,'erreur requete 4_3')

def find_edit_details_oeuvre_id_exemplaire(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_10' FROM DUAL '''
        cursor.execute(sql, (id))
        exemplaire = cursor.fetchone()
        return exemplaire
    except ValueError:
        abort(400,'erreur requete 4_10')


def exemplaire_insert(titre,dateParution,photo,idAuteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_5' FROM DUAL '''
        cursor.execute(sql, (titre,dateParution,photo,idAuteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_5')

def exemplaire_update(noOeuvre, etat, dateAchat, prix, id_exemplaire):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_12' FROM DUAL '''
        cursor.execute(sql, (noOeuvre, etat, dateAchat, prix, id_exemplaire))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_12')

def exemplaire_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete4_8' FROM DUAL '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 4_8')
