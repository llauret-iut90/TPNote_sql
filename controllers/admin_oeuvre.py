#! /usr/bin/python
# -*- coding:utf-8 -*-
import re
from flask import *
import datetime

import os
from models.dao_oeuvre import *
from models.dao_auteur import find_auteurs, find_one_auteur
from validator.validator_oeuvre_etu import *
from connexion_db import get_db

admin_oeuvre = Blueprint('admin_oeuvre', __name__,
                         template_folder='templates')


@admin_oeuvre.route('/admin/oeuvre/show')
def show_oeuvre():
    oeuvres = find_oeuvres()
    # print(articles)
    return render_template('admin/oeuvre/show_oeuvre.html', oeuvres=oeuvres)


@admin_oeuvre.route('/admin/oeuvre/add', methods=['GET'])
def add_oeuvre():
    auteurs = find_auteurs()
    return render_template('admin/oeuvre/add_oeuvre.html', auteurs=auteurs, donnees=[], erreurs=[])


@admin_oeuvre.route('/admin/oeuvre/add', methods=['POST'])
def valid_add_oeuvre():
    titre = request.form.get('titre', '')
    date_parution = request.form.get('date_parution', '')
    auteur_id = request.form.get('auteur_id', '')
    photo = request.form.get('photo', '')

    dto_data = {'titre': titre, 'photo': photo, 'date_parution': date_parution, 'auteur_id': auteur_id}
    valid, errors, dto_data = validator_oeuvre(dto_data)
    if valid:
        date_parution = dto_data['date_parution_iso']
        oeuvre_insert(titre, date_parution, photo, auteur_id)
        message = u'oeuvre ajouté , nom:' + titre + '- auteur_id:' + auteur_id + ' - photo:' + photo
        flash(message, 'success radius')
        return redirect('/admin/oeuvre/show')
    auteurs = find_auteurs()
    return render_template('admin/oeuvre/add_oeuvre.html', auteurs=auteurs, erreurs=errors, donnees=dto_data)


@admin_oeuvre.route('/admin/oeuvre/delete', methods=['GET'])
def delete_oeuvre():
    id_oeuvre = request.args.get('id_oeuvre', '')
    if not (id_oeuvre and id_oeuvre.isnumeric()):
        abort("404", "erreur id_oeuvre")

    nb_exemplaires = find_oeuvre_nbExemplaires(id_oeuvre)
    if nb_exemplaires == 0:
        oeuvre_delete(id_oeuvre)
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
    oeuvre = find_one_oeuvre(id_oeuvre)
    if oeuvre is None:
        abort(404, 'erreur sur id_oeuvre')
    if oeuvre['date_parution']:
        oeuvre['date_parution'] = oeuvre['date_parution'].strftime("%d/%m/%Y")
    auteurs = find_auteurs()
    return render_template('admin/oeuvre/edit_oeuvre.html', donnees=oeuvre, auteurs=auteurs, erreurs=[])


@admin_oeuvre.route('/admin/oeuvre/edit', methods=['POST'])
def valid_edit_oeuvre():
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
        oeuvre_update(titre, auteur_id, date_parution, photo, id_oeuvre)
        message = u'oeuvre modifiée , titre:' + titre + '- auteur_id:' + auteur_id
        flash(message, 'success radius')
        return redirect('/admin/oeuvre/show')
    auteurs = find_auteurs()
    return render_template('admin/oeuvre/edit_oeuvre.html', auteurs=auteurs, erreurs=errors, donnees=dto_data)
