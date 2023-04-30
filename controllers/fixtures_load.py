#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/admin/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS  ; '''

    mycursor.execute(sql)
    sql='''

CREATE TABLE adherent (
  
);
    '''
    mycursor.execute(sql)
    sql=''' 
CREATE TABLE auteur (

);
    '''
    mycursor.execute(sql)
    sql=''' 
CREATE TABLE oeuvre (

);
    '''
    mycursor.execute(sql)
    sql=''' 
CREATE TABLE exemplaire (
   
) ;  

    '''
    mycursor.execute(sql)
    sql=''' 
CREATE TABLE emprunt (

) ;  

    '''
    mycursor.execute(sql)
    auteurs = [{'id': 1, 'nom': 'Christie', 'prenom': 'Agatha'},
               {'id': 2, 'nom': 'Chateaubriand', 'prenom': 'François-René'},
               {'id': 3, 'nom': 'Flaubert', 'prenom': 'Gustave'},
               {'id': 4, 'nom': 'Prévert', 'prenom': 'Jacques'},
               {'id': 5, 'nom': 'De La Fontaine', 'prenom': 'Jean'},
               {'id': 6, 'nom': 'Daudet', 'prenom': 'Alphonse'},
               {'id': 7, 'nom': 'Hugo', 'prenom': 'Victor'},
               {'id': 8, 'nom': 'Kessel', 'prenom': 'Joseph'},
               {'id': 9, 'nom': 'Duras', 'prenom': 'Marguerite'},
               {'id': 10, 'nom': 'Proust', 'prenom': 'Marcel'},
               {'id': 11, 'nom': 'Zola', 'prenom': 'Émile'},
               {'id': 12, 'nom': 'Highsmith', 'prenom': 'Patricia'},
               {'id': 13, 'nom': 'Kipling', 'prenom': 'Rudyard'},
               {'id': 14, 'nom': 'Azimov', 'prenom': 'Isaac'},
               {'id': 15, 'nom': 'Baudelaire', 'prenom': 'Charles'},
               {'id': 16, 'nom': 'Moliere', 'prenom': 'Jean-Baptiste Poquelin'}]

    for enr_auteur in auteurs:
        tuple_insert = (enr_auteur['nom'], enr_auteur['prenom'])
        sql = "INSERT INTO auteur (nom,prenom) VALUES (%s,%s)"
        mycursor.execute(sql, tuple_insert)
    get_db().commit()


    adherents = [{'id': 1, 'nom': 'billot', 'adresse': 'Montbeliard', 'date_paiement': datetime.date(2022, 11, 3)},
                 {'id': 2, 'nom': 'lauvernay', 'adresse': 'sevenans', 'date_paiement': datetime.date(2022, 6, 13)},
                 {'id': 3, 'nom': 'axelrad', 'adresse': 'sevenans', 'date_paiement': datetime.date(2022, 1, 12)},
                 {'id': 4, 'nom': 'bedez', 'adresse': 'hericourt', 'date_paiement': datetime.date(2022, 4, 17)},
                 {'id': 5, 'nom': 'berger', 'adresse': 'les glacis', 'date_paiement': datetime.date(2013, 11, 3)},
                 {'id': 6, 'nom': 'cambot', 'adresse': 'sevenans', 'date_paiement': datetime.date(2022, 12, 15)},
                 {'id': 7, 'nom': 'bonilla', 'adresse': 'sochaux', 'date_paiement': datetime.date(2022, 2, 17)},
                 {'id': 8, 'nom': 'asproitis', 'adresse': 'grenoble', 'date_paiement': datetime.date(2022, 12, 4)},
                 {'id': 9, 'nom': 'pereira', 'adresse': 'danjoutin', 'date_paiement': datetime.date(2022, 11, 3)},
                 {'id': 10, 'nom': 'dupont', 'adresse': 'grenoble', 'date_paiement': datetime.date(2022, 3, 14)},
                 {'id': 11, 'nom': 'durant', 'adresse': 'belfort', 'date_paiement': datetime.date(2022, 12, 16)},
                 {'id': 12, 'nom': 'piton', 'adresse': 'belfort', 'date_paiement': datetime.date(2022, 11, 3)}]

    for enr_adherent in adherents:
        tuple_insert = (enr_adherent['nom'], enr_adherent['adresse'], enr_adherent['date_paiement'])
        sql = "INSERT INTO adherent (nom,adresse,date_paiement) VALUES (%s,%s,%s)"
        mycursor.execute(sql, tuple_insert)
    get_db().commit()

    oeuvres = [{'id': 1, 'titre': 'le retour de Poirot', 'date_parution': datetime.date(1960, 2, 12),
                'photo': 'leRetourDePoirot.jpg', 'auteur_id': 1},
               {'id': 2, 'titre': 'Poirot quitte la scène', 'date_parution': datetime.date(1975, 5, 1), 'photo': '',
                'auteur_id': 1},
               {'id': 3, 'titre': 'dix brèves rencontres', 'date_parution': datetime.date(1982, 10, 1),
                'photo': 'dixBrevesRencontres.jpg', 'auteur_id': 1},
               {'id': 4, 'titre': 'le miroir de la mort', 'date_parution': datetime.date(1961, 1, 1),
                'photo': 'leMiroirDuMort.jpeg', 'auteur_id': 1},
               {'id': 6, 'titre': 'une créature de rêve', 'date_parution': datetime.date(1992, 2, 1), 'photo': '',
                'auteur_id': 12},
               {'id': 7, 'titre': "mémoire d'outre-tombe", 'date_parution': datetime.date(1949, 1, 1), 'photo': '',
                'auteur_id': 2},
               {'id': 8, 'titre': 'Madame de Bovary', 'date_parution': datetime.date(1956, 12, 15), 'photo': '',
                'auteur_id': 3},
               {'id': 9, 'titre': 'un amour de swam', 'date_parution': datetime.date(2004, 6, 1),
                'photo': 'unAmourDeSwann.jpeg', 'auteur_id': 9},
               {'id': 10, 'titre': 'les femmes savantes', 'date_parution': datetime.date(1672, 3, 16), 'photo': '',
                'auteur_id': 16},
               {'id': 11, 'titre': 'le misanthrope', 'date_parution': datetime.date(1666, 1, 1), 'photo': '',
                'auteur_id': 16},
               {'id': 12, 'titre': 'Les fleurs du mal', 'date_parution': datetime.date(1957, 6, 25),
                'photo': 'lesFleursDuMal.jpg', 'auteur_id': 15},
               {'id': 13, 'titre': 'petits poèmes en prose', 'date_parution': datetime.date(1969, 1, 1), 'photo': '',
                'auteur_id': 15},
               {'id': 14, 'titre': 'les mondes perdus', 'date_parution': datetime.date(1980, 5, 6),
                'photo': 'lesMondesPerdus.jpg', 'auteur_id': 14},
               {'id': 15, 'titre': 'La guerre des mondes', 'date_parution': datetime.date(1970, 3, 15), 'photo': '',
                'auteur_id': 14},
               {'id': 16, 'titre': 'spectacles', 'date_parution': datetime.date(1948, 5, 12), 'photo': '',
                'auteur_id': 4},
               {'id': 17, 'titre': 'Les fables', 'date_parution': datetime.date(1694, 1, 1), 'photo': '',
                'auteur_id': 5},
               {'id': 18, 'titre': "Le triomphe de l'amour", 'date_parution': datetime.date(1980, 5, 6), 'photo': '',
                'auteur_id': 5},
               {'id': 19, 'titre': 'le livre de la jungle', 'date_parution': datetime.date(1968, 12, 11), 'photo': '',
                'auteur_id': 13},
               {'id': 20, 'titre': 'kim', 'date_parution': datetime.date(1901, 7, 1), 'photo': '', 'auteur_id': 13},
               {'id': 21, 'titre': 'le marin de Gibraltar', 'date_parution': datetime.date(1952, 7, 12), 'photo': '',
                'auteur_id': 9},
               {'id': 22, 'titre': 'l’assommoir', 'date_parution': datetime.date(1976, 1, 1), 'photo': '',
                'auteur_id': 11},
               {'id': 23, 'titre': "j'accuse", 'date_parution': datetime.date(1898, 1, 13), 'photo': '',
                'auteur_id': 11},
               {'id': 24, 'titre': 'la terre', 'date_parution': datetime.date(1887, 1, 1), 'photo': '',
                'auteur_id': 11}]

    for enr_oeuvre in oeuvres:
        tuple_insert = (enr_oeuvre['titre'], enr_oeuvre['date_parution'], enr_oeuvre['photo'], enr_oeuvre['auteur_id'])
        sql = ""
        mycursor.execute(sql, tuple_insert)
    get_db().commit()

    exemplaires = [
        {'id': 1, 'etat': 'BON', 'date_achat': datetime.date(2022, 8, 25), 'prix': Decimal('13.50'), 'oeuvre_id': 1},
        {'id': 2, 'etat': 'MOYEN', 'date_achat': datetime.date(2015, 9, 28), 'prix': Decimal('12.50'), 'oeuvre_id': 1},
        {'id': 3, 'etat': 'MOYEN', 'date_achat': datetime.date(2022, 5, 26), 'prix': Decimal('12.00'), 'oeuvre_id': 1},
        {'id': 4, 'etat': 'BON', 'date_achat': datetime.date(2015, 1, 11), 'prix': Decimal('10.00'), 'oeuvre_id': 1},
        {'id': 5, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2021, 10, 29), 'prix': Decimal('13.00'),
         'oeuvre_id': 2},
        {'id': 6, 'etat': 'NEUF', 'date_achat': datetime.date(2022, 10, 29), 'prix': Decimal('20.00'), 'oeuvre_id': 2},
        {'id': 7, 'etat': 'BON', 'date_achat': datetime.date(2021, 12, 27), 'prix': Decimal('7.00'), 'oeuvre_id': 3},
        {'id': 8, 'etat': 'MOYEN', 'date_achat': datetime.date(2021, 9, 25), 'prix': Decimal('13.00'), 'oeuvre_id': 3},
        {'id': 9, 'etat': 'NEUF', 'date_achat': datetime.date(2015, 12, 29), 'prix': Decimal('18.00'), 'oeuvre_id': 4},
        {'id': 10, 'etat': 'NEUF', 'date_achat': datetime.date(2015, 12, 29), 'prix': Decimal('21.00'), 'oeuvre_id': 4},
        {'id': 11, 'etat': 'BON', 'date_achat': datetime.date(2015, 4, 29), 'prix': Decimal('26.00'), 'oeuvre_id': 4},
        {'id': 12, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 24), 'prix': Decimal('22.00'), 'oeuvre_id': 6},
        {'id': 13, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 24), 'prix': Decimal('22.00'), 'oeuvre_id': 6},
        {'id': 14, 'etat': 'BON', 'date_achat': datetime.date(2022, 5, 1), 'prix': Decimal('28.00'), 'oeuvre_id': 7},
        {'id': 15, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2022, 1, 26), 'prix': Decimal('28.00'),
         'oeuvre_id': 7},
        {'id': 16, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 24), 'prix': Decimal('30.00'), 'oeuvre_id': 8},
        {'id': 17, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 23), 'prix': Decimal('32.00'), 'oeuvre_id': 9},
        {'id': 18, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2015, 1, 29), 'prix': Decimal('17.00'),
         'oeuvre_id': 10},
        {'id': 19, 'etat': 'BON', 'date_achat': datetime.date(2021, 10, 29), 'prix': Decimal('18.00'), 'oeuvre_id': 10},
        {'id': 20, 'etat': 'BON', 'date_achat': datetime.date(2021, 10, 29), 'prix': Decimal('18.00'), 'oeuvre_id': 10},
        {'id': 21, 'etat': 'BON', 'date_achat': datetime.date(2021, 10, 29), 'prix': Decimal('19.00'), 'oeuvre_id': 10},
        {'id': 22, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 26), 'prix': Decimal('20.00'), 'oeuvre_id': 11},
        {'id': 23, 'etat': 'BON', 'date_achat': datetime.date(2022, 10, 29), 'prix': Decimal('21.50'), 'oeuvre_id': 12},
        {'id': 24, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2022, 1, 24), 'prix': Decimal('22.00'),
         'oeuvre_id': 13},
        {'id': 25, 'etat': 'BON', 'date_achat': datetime.date(2015, 1, 28), 'prix': Decimal('22.00'), 'oeuvre_id': 13},
        {'id': 26, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2022, 1, 23), 'prix': Decimal('26.00'),
         'oeuvre_id': 14},
        {'id': 27, 'etat': 'MOYEN', 'date_achat': datetime.date(2015, 12, 26), 'prix': Decimal('13.00'),
         'oeuvre_id': 14},
        {'id': 28, 'etat': 'BON', 'date_achat': datetime.date(2022, 2, 23), 'prix': Decimal('12.00'), 'oeuvre_id': 15},
        {'id': 29, 'etat': 'BON', 'date_achat': datetime.date(2022, 10, 29), 'prix': Decimal('15.00'), 'oeuvre_id': 15},
        {'id': 30, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2022, 1, 26), 'prix': Decimal('32.00'),
         'oeuvre_id': 16},
        {'id': 31, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 23), 'prix': Decimal('19.00'), 'oeuvre_id': 17},
        {'id': 32, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2017, 10, 29), 'prix': Decimal('19.00'),
         'oeuvre_id': 17},
        {'id': 33, 'etat': 'BON', 'date_achat': datetime.date(2021, 1, 23), 'prix': Decimal('20.00'), 'oeuvre_id': 19},
        {'id': 34, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 25), 'prix': Decimal('11.00'), 'oeuvre_id': 19},
        {'id': 35, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2021, 10, 29), 'prix': Decimal('15.00'),
         'oeuvre_id': 19},
        {'id': 36, 'etat': 'NEUF', 'date_achat': datetime.date(2022, 10, 29), 'prix': Decimal('18.00'),
         'oeuvre_id': 19},
        {'id': 37, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 23), 'prix': Decimal('8.00'), 'oeuvre_id': 19},
        {'id': 38, 'etat': 'MAUVAIS', 'date_achat': datetime.date(2021, 9, 28), 'prix': Decimal('18.00'),
         'oeuvre_id': 20},
        {'id': 39, 'etat': 'BON', 'date_achat': datetime.date(2021, 12, 26), 'prix': Decimal('18.00'), 'oeuvre_id': 20},
        {'id': 40, 'etat': 'BON', 'date_achat': datetime.date(2022, 1, 23), 'prix': Decimal('11.00'), 'oeuvre_id': 20}]

    for enr_exemplaire in exemplaires:
        tuple_insert = (enr_exemplaire['etat'], enr_exemplaire['date_achat'], enr_exemplaire['prix'],
                                enr_exemplaire['oeuvre_id'])
        sql = ""
        mycursor.execute(sql, tuple_insert)
    get_db().commit()

    emprunts = [{'adherent_id': 6, 'exemplaire_id': 2, 'date_emprunt': datetime.date(2022, 9, 21),
                 'date_retour': datetime.date(2022, 9, 28)},
                {'adherent_id': 7, 'exemplaire_id': 2, 'date_emprunt': datetime.date(2022, 10, 21),
                 'date_retour': datetime.date(2022, 10, 28)},
                {'adherent_id': 8, 'exemplaire_id': 2, 'date_emprunt': datetime.date(2022, 11, 21),
                 'date_retour': datetime.date(2022, 11, 28)},
                {'adherent_id': 3, 'exemplaire_id': 3, 'date_emprunt': datetime.date(2022, 9, 13), 'date_retour': None},
                {'adherent_id': 2, 'exemplaire_id': 4, 'date_emprunt': datetime.date(2022, 12, 1), 'date_retour': None},
                {'adherent_id': 2, 'exemplaire_id': 5, 'date_emprunt': datetime.date(2022, 8, 23),
                 'date_retour': datetime.date(2022, 9, 23)},
                {'adherent_id': 2, 'exemplaire_id': 5, 'date_emprunt': datetime.date(2022, 12, 15),
                 'date_retour': None},
                {'adherent_id': 3, 'exemplaire_id': 5, 'date_emprunt': datetime.date(2022, 7, 26),
                 'date_retour': datetime.date(2022, 8, 23)},
                {'adherent_id': 3, 'exemplaire_id': 5, 'date_emprunt': datetime.date(2022, 11, 23),
                 'date_retour': datetime.date(2022, 12, 24)},
                {'adherent_id': 4, 'exemplaire_id': 6, 'date_emprunt': datetime.date(2023, 1, 22),
                 'date_retour': datetime.date(2023, 1, 23)},
                {'adherent_id': 4, 'exemplaire_id': 6, 'date_emprunt': datetime.date(2023, 1, 25), 'date_retour': None},
                {'adherent_id': 3, 'exemplaire_id': 7, 'date_emprunt': datetime.date(2023, 2, 22),
                 'date_retour': datetime.date(2023, 3, 29)},
                {'adherent_id': 2, 'exemplaire_id': 8, 'date_emprunt': datetime.date(2022, 12, 30),
                 'date_retour': None},
                {'adherent_id': 3, 'exemplaire_id': 9, 'date_emprunt': datetime.date(2023, 1, 25), 'date_retour': None},
                {'adherent_id': 8, 'exemplaire_id': 9, 'date_emprunt': datetime.date(2022, 7, 26),
                 'date_retour': datetime.date(2022, 9, 22)},
                {'adherent_id': 3, 'exemplaire_id': 11, 'date_emprunt': datetime.date(2023, 1, 26),
                 'date_retour': datetime.date(2023, 2, 21)},
                {'adherent_id': 3, 'exemplaire_id': 13, 'date_emprunt': datetime.date(2023, 1, 4), 'date_retour': None},
                {'adherent_id': 6, 'exemplaire_id': 15, 'date_emprunt': datetime.date(2022, 9, 23),
                 'date_retour': datetime.date(2022, 9, 26)},
                {'adherent_id': 2, 'exemplaire_id': 18, 'date_emprunt': datetime.date(2022, 9, 23),
                 'date_retour': datetime.date(2022, 10, 28)},
                {'adherent_id': 2, 'exemplaire_id': 19, 'date_emprunt': datetime.date(2023, 2, 26),
                 'date_retour': None},
                {'adherent_id': 4, 'exemplaire_id': 19, 'date_emprunt': datetime.date(2022, 9, 21),
                 'date_retour': None},
                {'adherent_id': 4, 'exemplaire_id': 27, 'date_emprunt': datetime.date(2023, 2, 22),
                 'date_retour': None},
                {'adherent_id': 3, 'exemplaire_id': 33, 'date_emprunt': datetime.date(2023, 1, 30),
                 'date_retour': None},
                {'adherent_id': 4, 'exemplaire_id': 34, 'date_emprunt': datetime.date(2023, 1, 23),
                 'date_retour': datetime.date(2023, 2, 20)},
                {'adherent_id': 2, 'exemplaire_id': 35, 'date_emprunt': datetime.date(2022, 7, 13),
                 'date_retour': datetime.date(2022, 9, 21)},
                {'adherent_id': 2, 'exemplaire_id': 37, 'date_emprunt': datetime.date(2023, 2, 11),
                 'date_retour': None},
                {'adherent_id': 7, 'exemplaire_id': 38, 'date_emprunt': datetime.date(2022, 7, 26),
                 'date_retour': datetime.date(2022, 10, 22)},
                {'adherent_id': 2, 'exemplaire_id': 40, 'date_emprunt': datetime.date(2023, 1, 23),
                 'date_retour': datetime.date(2023, 2, 23)},
                {'adherent_id': 3, 'exemplaire_id': 40, 'date_emprunt': datetime.date(2022, 11, 23),
                 'date_retour': datetime.date(2022, 12, 24)},
                {'adherent_id': 5, 'exemplaire_id': 40, 'date_emprunt': datetime.date(2022, 7, 25),
                 'date_retour': datetime.date(2022, 9, 22)},
                {'adherent_id': 9, 'exemplaire_id': 15, 'date_emprunt': datetime.date(2023, 2, 22),
                 'date_retour': None},
                {'adherent_id': 9, 'exemplaire_id': 18, 'date_emprunt': datetime.date(2023, 1, 30),
                 'date_retour': None}
                ]

    for enr_emprunt in emprunts:
        tuple_insert = (enr_emprunt['adherent_id'], enr_emprunt['exemplaire_id'], enr_emprunt['date_emprunt'],
                          enr_emprunt['date_retour'])
        sql = ""
        mycursor.execute(sql, tuple_insert)
    get_db().commit()

    return redirect('/')
