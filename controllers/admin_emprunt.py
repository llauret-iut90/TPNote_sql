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
        donnees_adherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents, action=action, erreurs=[])
    if action == 'rendre':
        sql = ''' SELECT 'requete5_2' FROM DUAL '''
        mycursor.execute(sql)
        donnees_adherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action=action, erreurs=[])
    abort(404,"erreur de paramètres")




@admin_emprunt.route('/admin/emprunt/emprunter', methods=['POST'])
def emprunt_emprunter():
    mycursor = get_db().cursor()
    donnees={}
    id_adherent = request.form.get('id_adherent', '')
    print(id_adherent)
    if id_adherent == '':
        sql = ''' SELECT 'requete5_1' FROM DUAL '''
        mycursor.execute(sql)
        donnees_adherents = mycursor.fetchall()
        erreurs={'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action='emprunter', erreurs=erreurs)

    sql = ''' SELECT 'requete5_3' FROM DUAL '''
    mycursor.execute(sql, (id_adherent))
    nbr_emprunt = mycursor.fetchone()

    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')
    tuple_insert = (id_adherent, date_emprunt, id_exemplaire)

    if id_adherent != '' and date_emprunt != '' and id_exemplaire !='' and nbr_emprunt['nbr_emprunt'] < 6 :
        # traitement des erreurs
        tuple_isert = (id_adherent,id_exemplaire,date_emprunt)
        print(tuple_insert)
        sql = ''' SELECT 'requete5_6' FROM DUAL '''
        mycursor.execute(sql, tuple_isert)
        get_db().commit()
        nbr_emprunt['nbr_emprunt']=nbr_emprunt['nbr_emprunt']+1

    sql = ''' SELECT 'requete5_7' FROM DUAL '''
    mycursor.execute(sql,(id_adherent))
    donnees_adherent = mycursor.fetchone()


    sql = ''' SELECT 'requete5_4' FROM DUAL '''
    mycursor.execute(sql)
    liste_exemp_dispo = mycursor.fetchall()

    sql = ''' SELECT 'requete5_5' FROM DUAL '''
    mycursor.execute(sql, (id_adherent))
    donnees_emprunt = mycursor.fetchall()

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
    mycursor = get_db().cursor()
    id_adherent = request.form.get('id_adherent', '')
    if id_adherent == '':
        sql = ''' SELECT 'requete5_2' FROM DUAL '''
        donnees_adherents = mycursor.fetchall()
        erreurs={'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                                   action='rendre', erreurs=erreurs)


    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')
    date_retour = request.form.get('date_retour', '')
    print(date_retour, id_adherent,date_emprunt,id_exemplaire)
    if id_adherent != '' and date_emprunt != '' and id_exemplaire !='' and date_retour != '' :
        # traitement des erreurs
        tuple_update = (date_retour, id_adherent,date_emprunt,id_exemplaire)
        print(tuple_update)
        sql = ''' SELECT 'requete5_8' FROM DUAL '''
        mycursor.execute(sql, tuple_update)
        get_db().commit()

    sql = ''' SELECT 'requete5_7' FROM DUAL '''
    mycursor.execute(sql,(id_adherent))
    donnees_adherent = mycursor.fetchone()
    sql = ''' SELECT 'requete5_3' FROM DUAL '''
    mycursor.execute(sql,(id_adherent))
    nbr_emprunts = mycursor.fetchone()
    sql = ''' SELECT 'requete5_5' FROM DUAL '''
    mycursor.execute(sql,(id_adherent))
    donnees_emprunts = mycursor.fetchall()

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
    mycursor = get_db().cursor()
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
                sql = ''' SELECT 'requete5_9' FROM DUAL '''
                mycursor.execute(sql, list_emprunts_split)
                if len(mycursor.fetchall()) != 1:
                    message = u'emprunt à supprimé, PB , oeuvre_id :' + str(elt)
                    flash(message)
                    return redirect('/admin/emprunt/delete')
                sql = ''' SELECT 'requete5_10' FROM DUAL '''
                mycursor.execute(sql, list_emprunts_split)
                get_db().commit()
            flash(u'emprunt(s) supprimé(s) : '+ str(nbr_suppr))
        if id_adherent.isnumeric():
            return redirect('/admin/emprunt/delete?id_adherent=' + str(id_adherent))
        return redirect('/admin/emprunt/delete')

    sql = ''' SELECT 'requete5_11' FROM DUAL '''
    param=[]
    if id_adherent.isnumeric():
        sql = sql + " WHERE adherent.id_adherent =  %s "
        param.append(id_adherent)
        print(param, id_adherent)
    sql=sql + " ORDER BY nom ASC, date_emprunt DESC;"
    print(sql, param)
    mycursor.execute(sql, param)
    donnees = mycursor.fetchall()
    sql = ''' SELECT 'requete5_12' FROM DUAL '''
    mycursor.execute(sql)
    donnees_adherents = mycursor.fetchall()
    if id_adherent.isnumeric():
            id_adherent = int(id_adherent)
    return render_template('admin/emprunt/delete_all_emprunts.html', donnees=donnees, donnees_adherents=donnees_adherents, id_adherent=id_adherent)




@admin_emprunt.route('/admin/emprunt/bilan-retard', methods=['GET'])
def bilan_emprunt():
    mycursor = get_db().cursor()
    sql = ''' SELECT 'requete5_13' FROM DUAL '''
    mycursor.execute(sql)
    donnees_bilan = mycursor.fetchall()
    return render_template('admin/emprunt/bilan_emprunt.html', donnees_bilan=donnees_bilan)











