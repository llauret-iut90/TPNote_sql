
from connexion_db import get_db
from flask import *

def find_adherents():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_1' FROM DUAL '''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 2_1')

def find_adherent_nbEmprunts(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_6' FROM DUAL '''
        cursor.execute(sql, (id))
        res_nb_emprunts = cursor.fetchone()
        if 'nb_emprunts' in res_nb_emprunts.keys():
            nb_emprunts=res_nb_emprunts['nb_emprunts']
            return nb_emprunts
    except ValueError:
        abort(400,'erreur requete 2_6')

def find_one_adherent(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_4' FROM DUAL '''
        cursor.execute(sql, (id))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete')


def adherent_insert(nom,adresse,datePaiement):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_2' FROM DUAL '''
        cursor.execute(sql, (nom,adresse,datePaiement))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 1_2')

def adherent_update(nom,adresse,datePaiement,id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_5' FROM DUAL '''
        cursor.execute(sql, (nom,adresse,datePaiement,id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 2_5')

def adherent_delete(id):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT 'requete2_3' FROM DUAL '''
        cursor.execute(sql, (id))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 2_3')
