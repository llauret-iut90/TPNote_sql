#! /usr/bin/python
# -*- coding:utf-8 -*-
import re
from flask import *
import datetime

import os

from connexion_db import get_db

admin_oeuvre = Blueprint('admin_oeuvre', __name__,
                         template_folder='templates')


@admin_oeuvre.route('/admin/oeuvre/show')
def show_oeuvre():
    mycursor = get_db().cursor()
    sql = '''  SELECT auteur.nom, oeuvre.titre, oeuvre.id_oeuvre, oeuvre.date_parution AS date_parution_iso
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
        GROUP BY oeuvre.id_oeuvre, auteur.nom, oeuvre.titre
        ORDER BY auteur.nom ASC, oeuvre.titre ASC;'''
    mycursor.execute(sql)
    oeuvres = mycursor.fetchall()
    # print(articles)
    return render_template('admin/oeuvre/show_oeuvre.html', oeuvres=oeuvres)


@admin_oeuvre.route('/admin/oeuvre/add', methods=['GET'])
def add_oeuvre():
    mycursor = get_db().cursor()
    sql = ''' SELECT id_auteur,nom FROM auteur ORDER BY nom'''
    mycursor.execute(sql)
    auteurs = mycursor.fetchall()
    return render_template('admin/oeuvre/add_oeuvre.html', auteurs=auteurs, donnees=[], erreurs=[])


@admin_oeuvre.route('/admin/oeuvre/add', methods=['POST'])
def valid_add_oeuvre():
    mycursor = get_db().cursor()
    titre = request.form.get('titre', '')
    date_parution = request.form.get('date_parution', '')
    auteur_id = request.form.get('auteur_id', '')
    photo = request.form.get('photo', '')

    dto_data = {'titre': titre, 'photo': photo, 'date_parution': date_parution, 'auteur_id': auteur_id}
    valid, errors, dto_data = validator_oeuvre(dto_data)
    if valid:
        date_parution = dto_data['date_parution_iso']
        tuple_insert = (titre, date_parution, photo, auteur_id)
        sql = ''' INSERT INTO oeuvre (titre, date_parution, photo, auteur_id) VALUES (%s,%s,%s,%s)'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'oeuvre ajouté , nom:' + titre + '- auteur_id:' + auteur_id + ' - photo:' + photo
        flash(message, 'success radius')
        return redirect('/admin/oeuvre/show')
    sql = ''' SELECT id_auteur,nom FROM auteur ORDER BY nom '''
    mycursor.execute(sql)
    auteurs = mycursor.fetchall()
    return render_template('admin/oeuvre/add_oeuvre.html', auteurs=auteurs, erreurs=errors, donnees=dto_data)


@admin_oeuvre.route('/admin/oeuvre/delete', methods=['GET'])
def delete_oeuvre():
    mycursor = get_db().cursor()
    id_oeuvre = request.args.get('id_oeuvre', '')
    if not (id_oeuvre and id_oeuvre.isnumeric()):
        abort("404", "erreur id_oeuvre")
    tuple_delete = (id_oeuvre,)

    nb_exemplaires = 0
    sql = ''' SELECT COUNT(exemplaire.id_exemplaire) AS nb_exemplaires 
    FROM oeuvre 
    INNER JOIN exemplaire ON oeuvre.id_oeuvre = exemplaire.oeuvre_id 
    WHERE oeuvre.id_oeuvre = %s  '''
    mycursor.execute(sql, tuple_delete)
    res_nb_exemplaires = mycursor.fetchone()
    if 'nb_exemplaires' in res_nb_exemplaires.keys():
        nb_exemplaires = res_nb_exemplaires['nb_exemplaires']
    if nb_exemplaires == 0:
        sql = ''' DELETE FROM oeuvre WHERE id_oeuvre = %s '''
        mycursor.execute(sql, tuple_delete)
        get_db().commit()
        message = 'supprimée, id: ' + id_oeuvre
        flash(message, 'success radius')
    else:
        message = u'suppression impossible, il faut supprimer  : ' + str(
            nb_exemplaires) + u' exemplaire(s) de cet oeuvre'
        flash(message, 'warning')
    return redirect('/admin/oeuvre/show')


@admin_oeuvre.route('/admin/oeuvre/edit', methods=['GET'])
def edit_oeuvre():
    id_oeuvre = request.args.get('id_oeuvre', '')
    mycursor = get_db().cursor()
    sql = ''' SELECT oeuvre.id_oeuvre, oeuvre.titre, oeuvre.date_parution, oeuvre.photo, oeuvre.auteur_id, auteur.nom 
    FROM oeuvre 
    INNER JOIN auteur ON oeuvre.auteur_id = auteur.id_auteur 
    WHERE oeuvre.id_oeuvre = %s '''
    mycursor.execute(sql, (id_oeuvre))
    oeuvre = mycursor.fetchone()
    if oeuvre is None:
        abort(404, 'erreur sur id_oeuvre')
    if oeuvre['date_parution']:
        oeuvre['date_parution'] = oeuvre['date_parution'].strftime("%d/%m/%Y")
    sql = ''' SELECT id_auteur,nom FROM auteur ORDER BY nom '''
    mycursor.execute(sql)
    auteurs = mycursor.fetchall()
    return render_template('admin/oeuvre/edit_oeuvre.html', donnees=oeuvre, auteurs=auteurs, erreurs=[])


@admin_oeuvre.route('/admin/oeuvre/edit', methods=['POST'])
def valid_edit_oeuvre():
    mycursor = get_db().cursor()
    id_oeuvre = request.form.get('id_oeuvre', '')
    titre = request.form.get('titre', '')
    date_parution = request.form.get('date_parution', '')
    auteur_id = request.form.get('auteur_id', '')
    photo = request.form.get('photo', '')
    dto_data = {'titre': titre, 'photo': photo, 'date_parution': date_parution, 'auteur_id': auteur_id,
                'id_oeuvre': id_oeuvre}
    print(dto_data)
    valid, errors, dto_data = validator_oeuvre(dto_data)
    if valid:
        date_parution = dto_data['date_parution_iso']
        tuple_update = (titre, auteur_id, date_parution, photo, id_oeuvre)
        print(tuple_update)
        sql = ''' UPDATE oeuvre SET titre=%s, auteur_id=%s, date_parution=%s, photo=%s WHERE id_oeuvre=%s '''
        mycursor.execute(sql, tuple_update)
        get_db().commit()
        message = u'oeuvre modifiée , titre:' + titre + '- auteur_id:' + auteur_id
        flash(message, 'success radius')
        return redirect('/admin/oeuvre/show')
    sql = ''' SELECT id_auteur,nom FROM auteur ORDER BY nom '''
    mycursor.execute(sql)
    auteurs = mycursor.fetchall()
    return render_template('admin/oeuvre/edit_oeuvre.html', auteurs=auteurs, erreurs=errors, donnees=dto_data)


def validator_oeuvre(data):
    mycursor = get_db().cursor()
    valid = True
    errors = dict()

    if 'auteur_id' in data.keys():
        if not data['auteur_id'].isdecimal():
            errors['auteur_id'] = 'type id incorrect'
            valid = False
    sql = ''' SELECT id_auteur,nom FROM auteur WHERE id_auteur = %s '''
    mycursor.execute(sql, (data['auteur_id'],))
    auteur = mycursor.fetchone()
    if not auteur:
        errors['auteur_id'] = "Saisir un Auteur"
        valid = False
    else:
        data['auteur_id'] = int(data['auteur_id'])

    if not re.match(r'\w{2,}', data['titre']):
        errors['titre'] = "Le titre doit avoir au moins deux caractères"
        valid = False

    try:
        datetime.datetime.strptime(data['date_parution'], '%d/%m/%Y')
    except ValueError:
        errors['date_parution'] = "la Date n'est pas valide format:%d/%m/%Y"
        valid = False
    else:
        data['date_parution_iso'] = datetime.datetime.strptime(data['date_parution'], "%d/%m/%Y").strftime("%Y-%m-%d")

    if data['photo']:
        photo_path = os.path.join(current_app.root_path,
                                  'static', 'assets', 'images', data['photo'])
        if not os.path.isfile(photo_path):
            errors['photo'] = f"la Photo n'existe pas: {photo_path}"
            valid = False
    return (valid, errors, data)
