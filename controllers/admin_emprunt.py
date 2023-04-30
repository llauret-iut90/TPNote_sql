#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from datetime import date

admin_emprunt = Blueprint('admin_emprunt', __name__,
                        template_folder='templates')

@admin_emprunt.route('/admin/emprunt/adherent-select')
def emprunt_select_adherent():
    mycursor = get_db().cursor()
    action = request.args.get('action', '')
    if action == 'emprunter':
        sql = ''' SELECT 'requete5_1' FROM DUAL '''
        mycursor.execute(sql)
        donneesAdherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donneesAdherents=donneesAdherents, action=action, erreurs=[])
    if action == 'rendre':
        sql = ''' SELECT 'requete5_2' FROM DUAL '''
        mycursor.execute(sql)
        donneesAdherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donneesAdherents=donneesAdherents,
                                   action=action, erreurs=[])
    abort(404,"erreur de paramètres")




@admin_emprunt.route('/admin/emprunt/emprunter', methods=['POST'])
def emprunt_emprunter():
    mycursor = get_db().cursor()
    donnees={}
    idAdherent = request.form.get('idAdherent', '')
    print(idAdherent)
    if idAdherent == '':
        sql = ''' SELECT 'requete5_1' FROM DUAL '''
        mycursor.execute(sql)
        donneesAdherents = mycursor.fetchall()
        erreurs={'idAdherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donneesAdherents=donneesAdherents,
                                   action='emprunter', erreurs=erreurs)

    sql = ''' SELECT 'requete5_3' FROM DUAL '''
    mycursor.execute(sql, (idAdherent))
    nbrEmprunts = mycursor.fetchone()

    dateEmprunt = request.form.get('dateEmprunt', '')
    noExemplaire = request.form.get('noExemplaire', '')
    tuple_isert = (idAdherent, dateEmprunt, noExemplaire)

    if idAdherent != '' and dateEmprunt != '' and noExemplaire !='' and nbrEmprunts['nbrEmprunt'] < 6 :
        # traitement des erreurs
        tuple_isert = (idAdherent,noExemplaire,dateEmprunt)
        print(tuple_isert)
        sql = ''' SELECT 'requete5_6' FROM DUAL '''
        mycursor.execute(sql, tuple_isert)
        get_db().commit()
        nbrEmprunts['nbrEmprunt']=nbrEmprunts['nbrEmprunt']+1

    sql = ''' SELECT 'requete5_7' FROM DUAL '''
    mycursor.execute(sql,(idAdherent))
    donneesAdherent = mycursor.fetchone()

    sql = ''' SELECT 'requete5_4' FROM DUAL '''
    mycursor.execute(sql)
    listeExempDispo = mycursor.fetchall()

    sql = ''' SELECT 'requete5_5' FROM DUAL '''
    mycursor.execute(sql, (idAdherent))
    donneesEmprunt = mycursor.fetchall()

    if 'dateEmprunt' not in donnees.keys() or donnees['dateEmprunt'] == '':
        donnees['dateEmprunt'] = date.today().strftime("%Y-%m-%d")

    return render_template('admin/emprunt/add_emprunts.html',
            donneesAdherent = donneesAdherent,
            action = 'emprunter',
            listeExempDispo = listeExempDispo,
            donneesEmprunt = donneesEmprunt,
            nbrEmprunts = nbrEmprunts,
            donnees = donnees,
            erreurs = [])

@admin_emprunt.route('/admin/emprunt/rendre', methods=['POST'])
def emprunt_rendre():
    mycursor = get_db().cursor()
    idAdherent = request.form.get('idAdherent', '')
    if idAdherent == '':
        sql = ''' SELECT 'requete5_2' FROM DUAL '''
        mycursor.execute(sql)
        donneesAdherents = mycursor.fetchall()
        erreurs={'idAdherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donneesAdherents=donneesAdherents,
                                   action='rendre', erreurs=erreurs)


    dateEmprunt = request.form.get('dateEmprunt', '')
    noExemplaire = request.form.get('noExemplaire', '')
    dateRetour = request.form.get('dateRetour', '')

    if idAdherent != '' and dateEmprunt != '' and noExemplaire !='' and dateRetour != '' :
        # traitement des erreurs
        tuple_update = (dateRetour, idAdherent,dateEmprunt,noExemplaire)
        print(tuple_update)
        sql = ''' SELECT 'requete5_8' FROM DUAL '''
        mycursor.execute(sql, tuple_update)
        get_db().commit()

    sql = ''' SELECT 'requete5_7' FROM DUAL '''
    mycursor.execute(sql,(idAdherent))
    donneesAdherent = mycursor.fetchone()
    sql = ''' SELECT 'requete5_3' FROM DUAL '''
    mycursor.execute(sql,(idAdherent))
    nbrEmprunts = mycursor.fetchone()
    sql = ''' SELECT 'requete5_5' FROM DUAL '''
    mycursor.execute(sql,(idAdherent))
    donneesEmprunts = mycursor.fetchall()

    donnees={}
    if 'dateRetour' not in donnees.keys() or donnees['dateRetour'] == '':
        donnees['dateRetour'] = date.today().strftime("%Y-%m-%d")

    return render_template('admin/emprunt/return_emprunts.html' , donneesAdherents=donneesAdherent,
            action = 'rendre',
            donneesEmprunt = donneesEmprunts,
            nbrEmprunts = nbrEmprunts,
            donnees = donnees,
            erreurs = [])


@admin_emprunt.route('/admin/emprunt/delete', methods=['GET','POST'])
def delete_emprunt_valid():
    mycursor = get_db().cursor()
    idAdherent = request.args.get('idAdherent', 'pasid')
    if request.method == 'POST':
        list_emprunts=request.form.getlist('select_emprunt')
        if(len(list_emprunts)>0):
            print(list_emprunts)
            for elt in list_emprunts:
                list_emprunts_split=elt.split('_')
                print(list_emprunts_split)
                sql = ''' SELECT 'requete5_9' FROM DUAL '''
                mycursor.execute(sql, list_emprunts_split)
                if len(mycursor.fetchall()) != 1:
                    message = u'emprunt à supprimé, PB , oeuvre_id :' + str(elt)
                    flash(message)
                    return redirect('/admin/emprunt/delete')
                sql = ''' SELECT 'requete5_10' FROM DUAL '''
                mycursor.execute(sql, list_emprunts_split)
                get_db().commit()
            message = u'emprunt(s) supprimé(s)'
            flash(message)
        return redirect('/admin/emprunt/delete')

    sql = ''' SELECT 'requete5_11' FROM DUAL '''
    if idAdherent.isnumeric():
        sql = sql + " WHERE adherent.id ="+str(idAdherent)
    sql=sql + " ORDER BY adherent.nom, emprunt.date_emprunt"

    mycursor.execute(sql)
    donnees = mycursor.fetchall()
    sql = ''' SELECT 'requete5_12' FROM DUAL '''
    mycursor.execute(sql)
    donneesAdherents = mycursor.fetchall()
    return render_template('admin/emprunt/delete_all_emprunts.html', donnees=donnees, donneesAdherents=donneesAdherents)


@admin_emprunt.route('/admin/emprunt/bilan-retard', methods=['GET'])
def bilan_emprunt():
    mycursor = get_db().cursor()
    sql = ''' SELECT 'requete5_13' FROM DUAL '''
    mycursor.execute(sql)
    donneesBilan = mycursor.fetchall()
    return render_template('admin/emprunt/bilan_emprunt.html', donnees=donneesBilan)






