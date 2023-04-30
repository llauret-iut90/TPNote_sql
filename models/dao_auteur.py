from connexion_db import get_db
from flask import *

def find_auteurs():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT auteur.id_auteur,auteur.nom,auteur.prenom, COUNT(oeuvre.id_oeuvre) AS nbrOeuvre 
    FROM auteur 
    LEFT JOIN oeuvre ON auteur.id_auteur = oeuvre.auteur_id 
    GROUP BY auteur.id_auteur 
    ORDER BY auteur.nom'''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 1_1')

def find_auteur_nbOeuvres(id_auteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT count(id_oeuvre) AS nbrOeuvre FROM oeuvre WHERE auteur_id = %s'''
        cursor.execute(sql, (id_auteur))
        res_nb_oeuvres = cursor.fetchone()
        if 'nb_oeuvres' in res_nb_oeuvres.keys():
            nb_oeuvres=res_nb_oeuvres['nb_oeuvres']
            return nb_oeuvres
    except ValueError:
        abort(400,'erreur requete 1_6')

def find_one_auteur(id_auteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT id_auteur, nom, prenom FROM auteur WHERE id_auteur = %s; '''
        cursor.execute(sql, (id_auteur))
        return cursor.fetchone()
    except ValueError:
        abort(400,'erreur requete 1_4')

def find_auteurs_dropdown():
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' SELECT id_auteur, nom FROM auteur ORDER BY nom'''
        cursor.execute(sql)
        return cursor.fetchall()
    except ValueError:
        abort(400,'erreur requete 3_6')

def auteur_insert(nom, prenom):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' INSERT INTO auteur(nom,prenom) VALUES (%s,%s) '''
        cursor.execute(sql, (nom, prenom))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 1_2')


def auteur_update(id_auteur, nom, prenom):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' UPDATE auteur SET nom = %s, prenom = %s WHERE id_auteur = %s '''
        cursor.execute(sql, (nom, prenom, id_auteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 1_5')

def auteur_delete(id_auteur):
    connection = get_db()
    try:
        cursor=connection.cursor()
        sql = ''' DELETE FROM auteur WHERE id_auteur = %s '''
        cursor.execute(sql, (id_auteur))
        connection.commit()
    except ValueError:
        abort(400,'erreur requete 1_3')







