#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from flask import *
import re
import datetime

from connexion_db import get_db

admin_exemplaire = Blueprint('admin_exemplaire', __name__,
                             template_folder='templates')


@admin_exemplaire.route('/admin/exemplaire/show')
def show_exemplaire():
    id_oeuvre = request.args.get('id_oeuvre', '')
    mycursor = get_db().cursor()
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
    mycursor.execute(sql, (id_oeuvre))
    oeuvre = mycursor.fetchone()
    sql = ''' SELECT exemplaire.id_exemplaire,
       exemplaire.date_achat,
       exemplaire.etat,
       exemplaire.oeuvre_id,
       exemplaire.id_exemplaire,
       oeuvre.date_parution,
       exemplaire.prix,
       COUNT(E1.id_exemplaire)                        AS ExemplaireDispo,
       IF(COUNT(E1.id_exemplaire) IS NULL, 'abs', 'present') AS present
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
    mycursor.execute(sql, (id_oeuvre))
    exemplaires = mycursor.fetchall()
    return render_template('admin/exemplaire/show_exemplaires.html', exemplaires=exemplaires, oeuvre=oeuvre)


@admin_exemplaire.route('/admin/exemplaire/add', methods=['GET'])
def add_exemplaire():
    id_oeuvre = request.args.get('id_oeuvre', '')
    mycursor = get_db().cursor()
    sql = ''' SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre
        FROM oeuvre
        JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
        LEFT JOIN exemplaire AS E1 ON E1.oeuvre_id = oeuvre.id_oeuvre
        WHERE oeuvre.id_oeuvre=%s
        GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
        ORDER BY auteur.nom, oeuvre.titre; '''
    mycursor.execute(sql, (id_oeuvre))
    oeuvre = mycursor.fetchone()
    date_achat = datetime.datetime.now().strftime("%d/%m/%Y")
    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre,
                           exemplaire={'date_achat': date_achat, 'id_oeuvre': id_oeuvre}, erreurs=[])


@admin_exemplaire.route('/admin/exemplaire/add', methods=['POST'])
def valid_add_exemplaire():
    mycursor = get_db().cursor()
    id_oeuvre = request.form.get('id_oeuvre', '')
    id_oeuvre = int(float(id_oeuvre))
    date_achat = request.form.get('date_achat', '')
    etat = request.form.get('etat', '')
    prix = request.form.get('prix', '')

    dto_data = {'id_oeuvre': id_oeuvre, 'etat': etat, 'date_achat': date_achat, 'prix': prix}
    valid, errors, dto_data = validator_exemplaire(dto_data)
    if valid:
        date_achat = dto_data['date_achat_iso']
        tuple_insert = (id_oeuvre, etat, date_achat, prix)
        print(tuple_insert)
        sql = ''' INSERT INTO exemplaire (oeuvre_id, etat, date_achat, prix) VALUES (%s, %s, %s, %s) '''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'exemplaire ajouté , oeuvre_id :' + str(id_oeuvre)
        flash(message, 'success radius')
        return redirect('/admin/exemplaire/show?id_oeuvre=' + str(id_oeuvre))

    sql = ''' SELECT COUNT(oeuvre.id_oeuvre) FROM oeuvre WHERE oeuvre.id_oeuvre=%s '''
    mycursor.execute(sql, (id_oeuvre))
    oeuvre = mycursor.fetchone()
    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre,
                           exemplaire=dto_data, erreurs=errors)


@admin_exemplaire.route('/admin/exemplaire/delete', methods=['GET'])
def delete_exemplaire():
    mycursor = get_db().cursor()
    id_exemplaire = request.args.get('id_exemplaire', '')
    tuple_delete = (id_exemplaire,)
    # sql = ''' SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution_iso
    #         , COALESCE (oeuvre.photo, '') AS photo
    #         , COUNT(E1.id_exemplaire) AS nb_exemplaire
    #         , COUNT(E2.id_exemplaire) AS nb_exemp_dispo
    #         , CONCAT(LPAD(CAST(DAY(oeuvre.date_parution)AS CHAR(2)),2,0),'/',LPAD(MONTH(oeuvre.date_parution), 2, '0'),'/', YEAR(oeuvre.date_parution))
    #         AS date_parution
    #         FROM oeuvre
    #         JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
    #         LEFT JOIN exemplaire AS E1 ON E1.oeuvre_id = oeuvre.id_oeuvre
    #         LEFT JOIN exemplaire AS E2 ON E2.id_exemplaire = E1.id_exemplaire
    #         AND E2.id_exemplaire
    #         NOT IN (SELECT emprunt.exemplaire_id FROM emprunt WHERE emprunt.date_retour IS NULL)
    #         WHERE oeuvre.id_oeuvre=%s
    #         GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
    #         ORDER BY auteur.nom, oeuvre.titre; '''
    sql = '''
    SELECT oeuvre_id FROM exemplaire WHERE id_exemplaire =%s
    '''
    mycursor.execute(sql, tuple_delete)
    oeuvre = mycursor.fetchone()
    oeuvre_id = str(oeuvre['oeuvre_id'])
    print(oeuvre, oeuvre_id)
    if not (oeuvre_id and oeuvre_id.isnumeric()):
        abort("404", "erreur id_oeuvre")
    nb_emprunts = 0
    sql = ''' SELECT COUNT(emprunt.exemplaire_id) AS nb_emprunts FROM emprunt WHERE emprunt.exemplaire_id=%s '''
    mycursor.execute(sql, tuple_delete)
    res_nb_emprunts = mycursor.fetchone()
    if 'nb_emprunts' in res_nb_emprunts.keys():
        nb_emprunts = res_nb_emprunts['nb_emprunts']
    if nb_emprunts == 0:
        sql = ''' DELETE FROM exemplaire WHERE id_exemplaire=%s'''
        mycursor.execute(sql, tuple_delete)
        get_db().commit()
        message = u'oeuvre supprimée, id: ' + id_exemplaire
        flash(message, 'success radius')
    else:
        message = u'suppression impossible, il faut supprimer  : ' + str(nb_emprunts) + u' emprunt(s) de cet exemplaire'
        flash(message, 'warning')
    return redirect('/admin/exemplaire/show?id_oeuvre=' + oeuvre_id)


@admin_exemplaire.route('/admin/exemplaire/edit', methods=['GET'])
def edit_exemplaire():
    mycursor = get_db().cursor()
    id_exemplaire = request.args.get('id_exemplaire', '')
    sql = ''' SELECT id_exemplaire, oeuvre_id, etat, date_achat, prix, auteur.nom, oeuvre.titre 
    FROM exemplaire
    INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
    INNER JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
    WHERE id_exemplaire=%s '''
    mycursor.execute(sql, (id_exemplaire))
    oeuvre = mycursor.fetchone()
    sql = ''' SELECT * FROM exemplaire WHERE id_exemplaire=%s '''
    mycursor.execute(sql, (id_exemplaire,))
    exemplaire = mycursor.fetchone()
    if exemplaire['date_achat']:
        exemplaire['date_achat'] = exemplaire['date_achat'].strftime("%d/%m/%Y")
    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=exemplaire, oeuvre=oeuvre, erreurs=[])


@admin_exemplaire.route('/admin/exemplaire/edit', methods=['POST'])
def valid_edit_exemplaire():
    mycursor = get_db().cursor()
    id_exemplaire = request.form.get('id_exemplaire', '')
    oeuvre_id = request.form.get('oeuvre_id', '')
    date_achat = request.form.get('date_achat', '')
    etat = request.form.get('etat', '')
    prix = request.form.get('prix', '')

    dto_data = {'oeuvre_id': oeuvre_id, 'etat': etat, 'date_achat': date_achat, 'prix': prix,
                'id_exemplaire': id_exemplaire}
    valid, errors, dto_data = validator_exemplaire(dto_data)
    print(valid, errors, dto_data)
    if valid:
        date_achat = dto_data['date_achat_iso']
        tuple_update = (oeuvre_id, etat, date_achat, prix, id_exemplaire)
        print(tuple_update)
        sql = ''' UPDATE exemplaire SET oeuvre_id=%s, etat=%s, date_achat=%s, prix=%s WHERE id_exemplaire=%s '''
        mycursor.execute(sql, tuple_update)
        get_db().commit()
        message = u' exemplaire modifié, id_exemplaire: ' + id_exemplaire
        flash(message, 'success radius')
        return redirect('/admin/exemplaire/show?id_oeuvre=' + oeuvre_id)
    sql = ''' SELECT id_exemplaire, oeuvre_id, etat, date_achat, prix, auteur.nom, oeuvre.titre 
    FROM exemplaire
    INNER JOIN oeuvre ON oeuvre.id_oeuvre = exemplaire.oeuvre_id
    INNER JOIN auteur ON auteur.id_auteur = oeuvre.auteur_id
    WHERE id_exemplaire=%s  '''
    mycursor.execute(sql, oeuvre_id)
    oeuvre = mycursor.fetchone()
    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=dto_data, oeuvre=oeuvre, erreurs=errors)


def validator_exemplaire(data):
    valid = True
    errors = dict()
    if 'id_exemplaire' in data.keys():
        if not data['id_exemplaire'].isnumeric():
            errors['id_exemplaire'] = 'type id incorrect(numeric)'
            valid = False
    if not re.match(r'\w{2,}', data['etat']):
        errors['etat'] = "Le titre doit avoir au moins deux caractères"
        valid = False
    try:
        datetime.datetime.strptime(data['date_achat'], '%d/%m/%Y')
    except ValueError:
        errors['date_achat'] = "la Date n'est pas valide format:%d/%m/%Y"
        valid = False
    else:
        data['date_achat_iso'] = datetime.datetime.strptime(data['date_achat'], "%d/%m/%Y").strftime("%Y-%m-%d")
    try:
        float(data['prix'])
    except ValueError:
        errors['prix'] = "le Prix n'est pas valide"
        valid = False
    return (valid, errors, data)
