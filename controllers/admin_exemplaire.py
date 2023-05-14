#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from flask import *
import re
import datetime
from models.dao_exemplaire import *
from validator.validator_exemplaire_etu import *

admin_exemplaire = Blueprint('admin_exemplaire', __name__,
                             template_folder='templates')


@admin_exemplaire.route('/admin/exemplaire/show')
def show_exemplaire():
    id_oeuvre = request.args.get('id_oeuvre', '')
    oeuvre = find_details_oeuvre_exemplaires(id_oeuvre)
    exemplaires = find_exemplaires_oeuvre(id_oeuvre)
    return render_template('admin/exemplaire/show_exemplaires.html', exemplaires=exemplaires, oeuvre=oeuvre)


@admin_exemplaire.route('/admin/exemplaire/add', methods=['GET'])
def add_exemplaire():
    id_oeuvre = request.args.get('id_oeuvre', '')
    oeuvre = find_add_exemplaire_info_oeuvre(id_oeuvre)
    date_achat = datetime.datetime.now().strftime("%d/%m/%Y")
    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre,
                           exemplaire={'date_achat': date_achat, 'id_oeuvre': id_oeuvre}, erreurs=[])


@admin_exemplaire.route('/admin/exemplaire/add', methods=['POST'])
def valid_add_exemplaire():
    id_oeuvre = request.form.get('id_oeuvre', '')
    id_oeuvre = int(float(id_oeuvre))
    date_achat = request.form.get('date_achat', '')
    etat = request.form.get('etat', '')
    prix = request.form.get('prix', '')

    dto_data = {'id_oeuvre': id_oeuvre, 'etat': etat, 'date_achat': date_achat, 'prix': prix}
    valid, errors, dto_data = validator_exemplaire(dto_data)
    if valid:
        date_achat = dto_data['date_achat_iso']
        exemplaire_insert(id_oeuvre, etat, date_achat, prix)
        message = u'exemplaire ajouté , oeuvre_id :' + str(id_oeuvre)
        flash(message, 'success radius')
        return redirect('/admin/exemplaire/show?id_oeuvre=' + str(id_oeuvre))

    oeuvre = find_id_oeuvre_exemplaire(id_oeuvre)
    return render_template('admin/exemplaire/add_exemplaire.html', oeuvre=oeuvre,
                           exemplaire=dto_data, erreurs=errors)


@admin_exemplaire.route('/admin/exemplaire/delete', methods=['GET'])
def delete_exemplaire():
    id_exemplaire = request.args.get('id_exemplaire', '')
    oeuvre = find_edit_one_exemplaire(id_exemplaire)
    oeuvre_id = str(oeuvre['oeuvre_id'])
    print(oeuvre, oeuvre_id)
    if not (oeuvre_id and oeuvre_id.isnumeric()):
        abort("404", "erreur id_oeuvre")
    nb_emprunts = find_exemplaire_nbEmprunts(id_exemplaire)

    if nb_emprunts == 0:
        exemplaire_delete(id_exemplaire)
        message = u'oeuvre supprimée, id: ' + id_exemplaire
        flash(message, 'success radius')
    else:
        message = u'suppression impossible, il faut supprimer  : ' + str(nb_emprunts) + u' emprunt(s) de cet exemplaire'
        flash(message, 'warning')
    return redirect('/admin/exemplaire/show?id_oeuvre=' + oeuvre_id)


@admin_exemplaire.route('/admin/exemplaire/edit', methods=['GET'])
def edit_exemplaire():
    id_exemplaire = request.args.get('id_exemplaire', '')
    oeuvre = find_edit_details_oeuvre_id_exemplaire(id_exemplaire)
    exemplaire = find_edit_one_exemplaire(id_exemplaire)
    if exemplaire['date_achat']:
        exemplaire['date_achat'] = exemplaire['date_achat'].strftime("%d/%m/%Y")
    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=exemplaire, oeuvre=oeuvre, erreurs=[])


@admin_exemplaire.route('/admin/exemplaire/edit', methods=['POST'])
def valid_edit_exemplaire():
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
        exemplaire_update(oeuvre_id, etat, date_achat, prix, id_exemplaire)
        message = u' exemplaire modifié, id_exemplaire: ' + id_exemplaire
        flash(message, 'success radius')
        return redirect('/admin/exemplaire/show?id_oeuvre=' + oeuvre_id)

    oeuvre = find_edit_details_oeuvre_id_exemplaire(id_exemplaire)
    return render_template('admin/exemplaire/edit_exemplaire.html', exemplaire=dto_data, oeuvre=oeuvre, erreurs=errors)

