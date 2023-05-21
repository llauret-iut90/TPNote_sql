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
        # 5.1
        sql = ''' SELECT ad.id_adherent,ad.nom,ad.date_paiement
FROM adherent ad
LEFT JOIN emprunt em on ad.id_adherent = em.adherent_id
WHERE (ad.date_paiement+INTERVAL 1 YEAR > CURDATE()) AND ad.id_adherent NOT IN (
SELECT DISTINCT em.adherent_id
FROM emprunt em
WHERE DATEDIFF(IFNULL(em.date_retour, CURDATE()), em.date_emprunt) > 90
GROUP BY em.adherent_id
HAVING COUNT(em.adherent_id) < 6
    ) AND ad.id_adherent NOT IN (SELECT adherent_id FROM emprunt 
    WHERE date_retour IS NULL GROUP BY adherent_id HAVING COUNT(adherent_id) >=5)
GROUP BY ad.id_adherent,ad.nom,ad.date_paiement
ORDER BY ad.nom; '''
        mycursor.execute(sql)
        donnees_adherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                               action=action, erreurs=[])
    if action == 'rendre':
        # 5.2
        sql = ''' SELECT DISTINCT adherent.id_adherent, adherent.nom
FROM adherent
         JOIN emprunt ON emprunt.adherent_id = adherent.id_adherent
         JOIN exemplaire ON exemplaire.id_exemplaire = emprunt.exemplaire_id
WHERE emprunt.date_retour IS NULL
ORDER BY adherent.nom; '''
        mycursor.execute(sql)
        donnees_adherents = mycursor.fetchall()
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                               action=action, erreurs=[])
    abort(404, "erreur de paramètres")


@admin_emprunt.route('/admin/emprunt/emprunter', methods=['POST'])
def emprunt_emprunter():
    mycursor = get_db().cursor()
    donnees = {}
    id_adherent = request.form.get('id_adherent', '')
    print(id_adherent)
    if id_adherent == '':
        # 5.1
        sql = ''' SELECT ad.id_adherent,ad.nom,ad.date_paiement
FROM adherent ad
LEFT JOIN emprunt em on ad.id_adherent = em.adherent_id
WHERE (ad.date_paiement+INTERVAL 1 YEAR > CURDATE()) AND ad.id_adherent NOT IN (
SELECT DISTINCT em.adherent_id
FROM emprunt em
WHERE DATEDIFF(IFNULL(em.date_retour, CURDATE()), em.date_emprunt) > 90
GROUP BY em.adherent_id
HAVING COUNT(em.adherent_id) < 6
    ) AND ad.id_adherent NOT IN (SELECT adherent_id FROM emprunt 
    WHERE date_retour IS NULL GROUP BY adherent_id HAVING COUNT(adherent_id) >=5)
GROUP BY ad.id_adherent,ad.nom,ad.date_paiement
ORDER BY ad.nom;  '''
        mycursor.execute(sql)
        donnees_adherents = mycursor.fetchall()
        erreurs = {'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                               action='emprunter', erreurs=erreurs)

    # 5.3
    sql = ''' SELECT COUNT(*) AS nbr_emprunt,
       SUM(CASE WHEN IFNULL(em.date_retour, NOW()) > em.date_emprunt + INTERVAL 90 DAY THEN 1 ELSE 0 END) AS retard
FROM emprunt em
WHERE em.adherent_id = %s AND em.date_retour IS NULL; '''
    mycursor.execute(sql, (id_adherent))
    nbr_emprunt = mycursor.fetchone()

    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')
    tuple_insert = (id_adherent, date_emprunt, id_exemplaire)

    if id_adherent != '' and date_emprunt != '' and id_exemplaire != '' and nbr_emprunt['nbr_emprunt'] < 6:
        # traitement des erreurs
        tuple_isert = (id_adherent, id_exemplaire, date_emprunt)
        print(tuple_insert)
        # 5.6
        sql = ''' INSERT INTO emprunt(adherent_id, exemplaire_id, date_emprunt)
VALUES (%s,%s,%s)'''
        mycursor.execute(sql, tuple_isert)
        get_db().commit()
        nbr_emprunt['nbr_emprunt'] = nbr_emprunt['nbr_emprunt'] + 1

    # 5.7
    sql = ''' SELECT id_adherent,nom,adresse,date_paiement
FROM adherent
WHERE id_adherent = %s '''
    mycursor.execute(sql, (id_adherent))
    donnees_adherent = mycursor.fetchone()

    # 5.4
    sql = ''' SELECT au.nom,oe.titre,oe.id_oeuvre AS noOeuvre,ex.id_exemplaire AS id_exemplaire
FROM exemplaire ex
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre
LEFT JOIN auteur au ON oe.auteur_id = au.id_auteur
WHERE ex.id_exemplaire NOT IN (
    SELECT exemplaire_id FROM emprunt WHERE date_retour IS NULL
    )
ORDER BY au.nom,oe.titre;'''
    mycursor.execute(sql)
    liste_exemp_dispo = mycursor.fetchall()

    # 5.5
    sql = ''' SELECT em.adherent_id AS id_adherent,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(CURDATE(), em.date_emprunt) as nb_jours_emprunt, em.date_emprunt
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON ex.id_exemplaire = em.exemplaire_id
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre
WHERE em.adherent_id = %s AND em.date_retour IS NULL
ORDER BY em.date_emprunt DESC;'''
    mycursor.execute(sql, (id_adherent))
    donnees_emprunt = mycursor.fetchall()

    if 'date_emprunt' not in donnees.keys() or donnees['date_emprunt'] == '':
        donnees['date_emprunt'] = date.today().strftime("%Y-%m-%d")
    return render_template('admin/emprunt/add_emprunts.html',
                           donnees_adherent=donnees_adherent,
                           action='emprunter',
                           liste_exemp_dispo=liste_exemp_dispo,
                           donnees_emprunt=donnees_emprunt,
                           nbr_emprunt=nbr_emprunt,
                           donnees=donnees,
                           erreurs=[])


@admin_emprunt.route('/admin/emprunt/rendre', methods=['POST'])
def emprunt_rendre():
    mycursor = get_db().cursor()
    id_adherent = request.form.get('id_adherent', '')
    if id_adherent == '':
        # 5.2
        sql = '''SELECT DISTINCT ad.nom,ad.id_adherent
FROM emprunt e
LEFT JOIN adherent ad on e.adherent_id = ad.id_adherent
WHERE e.date_retour IS NULL
ORDER BY ad.nom; '''
        donnees_adherents = mycursor.fetchall()
        erreurs = {'id_adherent': u'Selectionner un adhérent'}
        return render_template('admin/emprunt/select_adherent_emprunts.html', donnees_adherents=donnees_adherents,
                               action='rendre', erreurs=erreurs)

    date_emprunt = request.form.get('date_emprunt', '')
    id_exemplaire = request.form.get('id_exemplaire', '')
    date_retour = request.form.get('date_retour', '')
    print(date_retour, id_adherent, date_emprunt, id_exemplaire)
    if id_adherent != '' and date_emprunt != '' and id_exemplaire != '' and date_retour != '':
        # traitement des erreurs
        tuple_update = (date_retour, id_adherent, date_emprunt, id_exemplaire)
        print(tuple_update)
        # 5.8
        sql = ''' UPDATE emprunt
SET date_retour=%s
WHERE adherent_id=%s AND date_emprunt=%s AND exemplaire_id=%s '''
        mycursor.execute(sql, tuple_update)
        get_db().commit()

    # 5.7
    sql = ''' SELECT id_adherent,nom,adresse,date_paiement
FROM adherent
WHERE id_adherent = %s '''
    mycursor.execute(sql, (id_adherent))
    donnees_adherent = mycursor.fetchone()
    # 5.3
    sql = ''' SELECT COUNT(*) AS nbr_emprunt,
       SUM(CASE WHEN IFNULL(em.date_retour, NOW()) > em.date_emprunt + INTERVAL 90 DAY THEN 1 ELSE 0 END) AS retard
FROM emprunt em
WHERE em.adherent_id = %s AND em.date_retour IS NULL;  '''
    mycursor.execute(sql, (id_adherent))
    nbr_emprunts = mycursor.fetchone()
    # 5.5
    sql = ''' SELECT em.adherent_id AS id_adherent,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(CURDATE(), em.date_emprunt) as nb_jours_emprunt, em.date_emprunt
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON ex.id_exemplaire = em.exemplaire_id
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre
WHERE em.adherent_id = %s AND em.date_retour IS NULL
ORDER BY em.date_emprunt DESC;'''
    mycursor.execute(sql, (id_adherent))
    donnees_emprunts = mycursor.fetchall()

    donnees = {}
    if 'date_retour' not in donnees.keys() or donnees['date_retour'] == '':
        donnees['date_retour'] = date.today().strftime("%Y-%m-%d")

    return render_template('admin/emprunt/return_emprunts.html', donnees_adherent=donnees_adherent,
                           action='rendre',
                           donnees_emprunts=donnees_emprunts,
                           nbr_emprunts=nbr_emprunts,
                           donnees=donnees,
                           erreurs=[])


@admin_emprunt.route('/admin/emprunt/delete', methods=['GET', 'POST'])
def delete_emprunt_valid():
    mycursor = get_db().cursor()
    id_adherent = request.args.get('id_adherent', 'pasid')
    print("adherent", id_adherent)
    if request.method == 'POST':
        id_adherent = request.form.get('id_adherent', 'pasid')
        list_emprunts = request.form.getlist('select_emprunt')
        if (len(list_emprunts) > 0):
            print(list_emprunts)
            nbr_suppr = len(list_emprunts)
            for elt in list_emprunts:
                list_emprunts_split = elt.split('_')
                print(list_emprunts_split)
                # 5.9
                sql = ''' SELECT * FROM emprunt WHERE adherent_id = %s AND exemplaire_id = %s AND date_emprunt = %s '''
                mycursor.execute(sql, list_emprunts_split)
                if len(mycursor.fetchall()) != 1:
                    message = u'emprunt à supprimé, PB , oeuvre_id :' + str(elt)
                    flash(message)
                    return redirect('/admin/emprunt/delete')
                # 5.10
                sql = ''' DELETE FROM emprunt WHERE adherent_id = %s AND exemplaire_id = %s AND date_emprunt = %s '''
                mycursor.execute(sql, list_emprunts_split)
                get_db().commit()
            flash(u'emprunt(s) supprimé(s) : ' + str(nbr_suppr))
        if id_adherent.isnumeric():
            return redirect('/admin/emprunt/delete?id_adherent=' + str(id_adherent))
        return redirect('/admin/emprunt/delete')

    # 5.11
    sql = ''' SELECT em.adherent_id AS id_adherent,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(IFNULL(em.date_retour, CURDATE()), em.date_emprunt) AS nb_jours_emprunt
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON ex.id_exemplaire = em.exemplaire_id
LEFT JOIN oeuvre oe ON ex.oeuvre_id = oe.id_oeuvre '''
    param = []
    if id_adherent.isnumeric():
        sql = sql + " WHERE adherent.id_adherent =  %s "
        param.append(id_adherent)
        print(param, id_adherent)
    sql = sql + " ORDER BY nom ASC, date_emprunt DESC;"
    print(sql, param)
    mycursor.execute(sql, param)
    donnees = mycursor.fetchall()
    # 5.12
    sql = '''  SELECT id_adherent,nom FROM adherent ORDER BY nom; '''
    mycursor.execute(sql)
    donnees_adherents = mycursor.fetchall()
    if id_adherent.isnumeric():
        id_adherent = int(id_adherent)
    return render_template('admin/emprunt/delete_all_emprunts.html', donnees=donnees,
                           donnees_adherents=donnees_adherents, id_adherent=id_adherent)


@admin_emprunt.route('/admin/emprunt/bilan-retard', methods=['GET'])
def bilan_emprunt():
    mycursor = get_db().cursor()
    # 5.13
    sql = ''' SELECT em.adherent_id,em.exemplaire_id AS id_exemplaire,oe.titre,ad.nom,em.date_emprunt,em.date_retour, DATEDIFF(CURDATE(), em.date_emprunt) AS nbJoursEmprunt
    , DATEDIFF(CURDATE(), em.date_emprunt+ INTERVAL 90 DAY) AS retard, em.date_emprunt + INTERVAL 90 DAY AS dateRenduTheorique
    , IF(DATEDIFF(CURDATE(), em.date_emprunt) > 90, 1,0) AS flagRetard, IF(DATEDIFF(CURDATE(), em.date_emprunt) > 120, 1,0) AS flag_penalite
    , IF((DATEDIFF(CURDATE(), em.date_emprunt)-120)*0.5 <= 25, (DATEDIFF(CURDATE(), em.date_emprunt)-120)*0.5, 25) AS dette
FROM emprunt em
LEFT JOIN adherent ad on em.adherent_id = ad.id_adherent
LEFT JOIN exemplaire ex ON em.exemplaire_id = ex.id_exemplaire
LEFT JOIN oeuvre oe on ex.oeuvre_id = oe.id_oeuvre
WHERE em.date_retour IS NULL
HAVING nbJoursEmprunt > 90
ORDER BY RETARD DESC '''
    mycursor.execute(sql)
    donnees_bilan = mycursor.fetchall()
    return render_template('admin/emprunt/bilan_emprunt.html', donnees_bilan=donnees_bilan)
