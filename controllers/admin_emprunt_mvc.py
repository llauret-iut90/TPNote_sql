#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from datetime import date

from models.dao_emprunt import *

admin_emprunt = Blueprint('admin_emprunt', __name__,
                        template_folder='templates')

@admin_emprunt.route('/admin/emprunt/adherent-select')
def emprunt_select_adherent():
    action = request.args.get('action', '')
    if action == 'emprunter':
        donnees_adherents = find_adherents_emprunter()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents, action=action, erreurs=[])
    if action == 'rendre':
        donnees_adherents = find_adherents_rendre()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action=action, erreurs=[])
    abort(404,"erreur de paramètres")




@admin_emprunt.route('/admin/emprunt/emprunter', methods=['POST'])
def emprunt_emprunter():
    donnees={}
    id_adherent = request.form.get('id_adherent', '')
    print(id_adherent+'id_adherent')
    if id_adherent == '':
        donnees_adherents = find_adherents_emprunter()
        erreurs={'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action='emprunter', erreurs=erreurs)

    nbr_emprunt = find_adherent_nbre_emprunt_retardDatePaiment(id_adherent)

    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')

    if id_adherent != '' and date_emprunt != '' and id_exemplaire !='' and nbr_emprunt['nbr_emprunt'] < 6 :
        # traitement des erreurs
        emprunt_insert(id_adherent, id_exemplaire, date_emprunt)
        nbr_emprunt['nbr_emprunt']=nbr_emprunt['nbr_emprunt']+1

    donnees_adherent = find_adherent_data(id_adherent)

    liste_exemp_dispo = find_exemplaire_oeuvre_disponible()

    donnees_emprunt = find_emprunt_data_adherent(id_adherent)

    if 'date_emprunt' not in donnees.keys() or donnees['date_emprunt'] == '':
        donnees['date_emprunt'] = date.today().strftime("%Y-%m-%d")
    return render_template('admin/emprunt/add_emprunts.html',
            donnees_adherent = donnees_adherent,
            action = 'emprunter',
            liste_exemp_dispo = liste_exemp_dispo,
            donnees_emprunt = donnees_emprunt,
            nbr_emprunt = nbr_emprunt,
            donnees = donnees,
            erreurs = [])

@admin_emprunt.route('/admin/emprunt/rendre', methods=['POST'])
def emprunt_rendre():
    id_adherent = request.form.get('id_adherent', '')
    print(id_adherent+'id_adherent')
    if id_adherent == '':
        donnees_adherents = find_adherents_rendre()
        erreurs={'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action='rendre', erreurs=erreurs)


    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')
    date_retour = request.form.get('date_retour', '')
    print(date_retour, id_adherent,date_emprunt,id_exemplaire)
    if id_adherent != '' and date_emprunt != '' and id_exemplaire !='' and date_retour != '' :
        # traitement des erreurs
        emprunt_update(date_retour, id_adherent,date_emprunt,id_exemplaire)

    donnees_adherent = find_adherent_data(id_adherent)
    nbr_emprunts = find_adherent_nbre_emprunt_retardDatePaiment(id_adherent)
    donnees_emprunts = find_emprunt_data_adherent(id_adherent)

    donnees={}
    if 'date_retour' not in donnees.keys() or donnees['date_retour'] == '':
        donnees['date_retour'] = date.today().strftime("%Y-%m-%d")

    return render_template('admin/emprunt/return_emprunts.html' , donnees_adherent=donnees_adherent,
            action = 'rendre',
            donnees_emprunts = donnees_emprunts,
            nbr_emprunts = nbr_emprunts,
            donnees = donnees,
            erreurs = [])


@admin_emprunt.route('/admin/emprunt/delete', methods=['GET','POST'])
def delete_emprunt_valid():
    id_adherent = request.args.get('id_adherent', 'pasid')
    print("adherent",id_adherent)
    if request.method == 'POST':
        id_adherent = request.form.get('id_adherent', 'pasid')
        list_emprunts=request.form.getlist('select_emprunt')
        if(len(list_emprunts)>0):
            print(list_emprunts)
            nbr_suppr = len(list_emprunts)
            for elt in list_emprunts:
                list_emprunts_split=elt.split('_')
                print(list_emprunts_split)
                r5_9 = find_select_emprunt_split(list_emprunts_split)
                if len(r5_9) != 1:
                    message = u'emprunt à supprimé, PB , oeuvre_id :' + str(elt)
                    flash(message)
                    return redirect('/admin/emprunt/delete')
                print(list_emprunts_split[0])
                emprunt_delete(list_emprunts_split)
            flash(u'emprunt(s) supprimé(s) : '+ str(nbr_suppr))
        if id_adherent.isnumeric():
            return redirect('/admin/emprunt/delete?id_adherent=' + str(id_adherent))
        return redirect('/admin/emprunt/delete')

    donnees = find_adherents_select_emprunts(id_adherent)
    donnees_adherents = find_adherents_dropdown()
    if id_adherent.isnumeric():
            id_adherent = int(id_adherent)
    return render_template('admin/emprunt/delete_all_emprunts.html', donnees=donnees, donnees_adherents=donnees_adherents, id_adherent=id_adherent)




@admin_emprunt.route('/admin/emprunt/bilan-retard', methods=['GET'])
def bilan_emprunt():
    donnees_bilan = find_bilan_emprunt()
    return render_template('admin/emprunt/bilan_emprunt.html', donnees_bilan=donnees_bilan)