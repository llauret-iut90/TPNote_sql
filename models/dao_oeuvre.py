
from connexion_db import get_db
from flask import *

def find_oeuvres():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_1' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 3_1')

def find_oeuvre_nbExemplaires(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_7' FROM DUAL '''
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
        sql = ''' SELECT 'requete3_4' FROM DUAL '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 3_4')


def oeuvre_insert(titre,dateParution,photo,idAuteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_2' FROM DUAL '''
        cursor.execute(sql, (titre,dateParution,photo,idAuteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_2')

def oeuvre_update(titre,idAuteur,dateParution,photo,id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_5' FROM DUAL '''
        cursor.execute(sql, (titre,idAuteur,dateParution,photo,id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_5')

def oeuvre_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete3_3' FROM DUAL '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 3_3')
