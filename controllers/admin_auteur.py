#! /usr/bin/python
# -*- coding:utf-8 -*-
import re
from flask import *
from models.dao_auteur import *
from validator.validator_auteur_etu import *

# from connexion_db import get_db

admin_auteur = Blueprint('admin_auteur', __name__,
                         template_folder='templates')


@admin_auteur.route('/admin/auteur/show')
def show_auteur():
    auteurs = find_auteurs()
    return render_template('admin/auteur/show_auteurs.html', auteurs=auteurs)


@admin_auteur.route('/admin/auteur/add', methods=['GET'])
def add_auteur():
    erreurs = []
    donnees = []
    return render_template('admin/auteur/add_auteur.html', erreurs=erreurs, donnees=donnees)


@admin_auteur.route('/admin/auteur/add', methods=['POST'])
def valid_add_auteur():
    nom = request.form.get('nom', '')
    prenom = request.form.get('prenom', '')
    dto_data = {'nom': nom, 'prenom': prenom}
    valid, errors = validator_auteur(dto_data)
    if valid:
        find_auteurs_dropdown()
        auteur_insert(nom, prenom)
        message = u'auteur ajouté , nom :' + nom
        flash(message, 'success radius')
        return redirect('/admin/auteur/show')
    return render_template('admin/auteur/add_auteur.html', erreurs=errors, donnees=dto_data)


@admin_auteur.route('/admin/auteur/delete', methods=['GET'])
def delete_auteur():
    id_auteur = request.args.get('id', '')
    if not (id_auteur and id_auteur.isnumeric()):
        abort("404", "erreur id auteur")
    nb_oeuvres = 0
    find_auteur_nbOeuvres(id_auteur)
    if nb_oeuvres == 0:
        auteur_delete(id_auteur)
        message = u'auteur supprimé, id: ' + id_auteur
        flash(message, 'success radius')
    else:
        message = u'suppression impossible, il faut supprimer  : ' + str(nb_oeuvres) + u' oeuvre(s) de cet auteur'
        flash(message, 'warning')
    return redirect('/admin/auteur/show')


@admin_auteur.route('/admin/auteur/edit', methods=['GET'])
def edit_auteur():
    id = request.args.get('id', '')
    auteur = find_one_auteur(id)
    erreurs = []
    return render_template('admin/auteur/edit_auteur.html', donnees=auteur, erreurs=erreurs)

@admin_auteur.route('/admin/auteur/edit', methods=['POST'])
def valid_edit_auteur():
    nom = request.form.get('nom', '')
    prenom = request.form.get('prenom', '')
    id_auteur = request.form.get('id_auteur', '')
    dto_data = {'nom': nom, 'prenom': prenom, 'id_auteur': id_auteur}
    valid, errors = validator_auteur(dto_data)
    if valid:
        auteur_update(id_auteur, nom, prenom)
        message = u'auteur modifié, id: ' + id_auteur + " nom : " + nom
        flash(message, 'success radius')
        return redirect('/admin/auteur/show')
    return render_template('admin/auteur/edit_auteur.html', donnees=dto_data, erreurs=errors)
