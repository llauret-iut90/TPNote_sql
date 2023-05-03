#! /usr/bin/python
# -*- coding:utf-8 -*-
from models.dao_adherent import *
from validator.validator_adherent_etu import *

admin_adherent = Blueprint('admin_adherent', __name__,
                           template_folder='templates')


@admin_adherent.route('/admin/adherent/show')
def show_adherent():
    adherents = find_adherents()
    return render_template('admin/adherent/show_adherents.html', adherents=adherents)


@admin_adherent.route('/admin/adherent/add', methods=['GET'])
def add_adherent():
    erreurs = []
    donnees = []
    return render_template('admin/adherent/add_adherent.html', erreurs=erreurs, donnees=donnees)


@admin_adherent.route('/admin/adherent/add', methods=['POST'])
def valid_add_adherent():
    nom = request.form.get('nom', '')
    adresse = request.form.get('adresse', '')
    date_paiement = request.form.get('date_paiement', '')

    dto_data = {'nom': nom, 'adresse': adresse, 'date_paiement': date_paiement}
    valid, errors, dto_data = validator_adherent(dto_data)
    if valid:
        date_paiement = dto_data['date_paiement_us']
        adherent_insert(nom, adresse, date_paiement)
        return redirect('/admin/adherent/show')
    return render_template('admin/adherent/add_adherent.html', erreurs=errors, donnees=dto_data)


@admin_adherent.route('/admin/adherent/delete', methods=['GET'])
def delete_adherent():
    id_adherent = request.args.get('id_adherent', '')
    if not (id_adherent and id_adherent.isnumeric()):
        abort("404", "erreur id adherent")
    nb_emprunts = find_adherent_nbEmprunts(id_adherent)
    if nb_emprunts == 0:
        adherent_delete(id_adherent)
        message = u'adherent supprimé, id_adherent: ' + id_adherent
        flash(message, 'success radius')
    else:
        message = u'suppression impossible, il faut supprimer  : ' + str(nb_emprunts) + u' emprunt(s) de cet adherent'
        flash(message, 'warning')
    return redirect('/admin/adherent/show')


@admin_adherent.route('/admin/adherent/edit', methods=['GET'])
def edit_adherent():
    id_adherent = request.args.get('id_adherent', '')
    adherent = find_one_adherent(id_adherent)
    if adherent['date_paiement']:
        adherent['date_paiement'] = adherent['date_paiement'].strftime("%d/%m/%Y")
    erreurs = []
    return render_template('admin/adherent/edit_adherent.html', donnees=adherent, erreurs=erreurs)


@admin_adherent.route('/admin/adherent/edit', methods=['POST'])
def valid_edit_adherent():
    id_adherent = request.form.get('id_adherent', '')
    nom = request.form.get('nom', '')
    adresse = request.form.get('adresse', '')
    date_paiement = request.form.get('date_paiement', '')
    dto_data = {'nom': nom, 'adresse': adresse, 'date_paiement': date_paiement, 'id_adherent': id_adherent}
    valid, errors, dto_data = validator_adherent(dto_data)
    if valid:
        date_paiement = dto_data['date_paiement_us']
        adherent_update(nom, adresse, date_paiement, id_adherent)
        message = u'adherent modifié, id_adherent: ' + id_adherent + " nom : " + nom
        flash(message, 'success radius')
        return redirect('/admin/adherent/show')
    return render_template('admin/adherent/edit_adherent.html', erreurs=errors, donnees=dto_data)
