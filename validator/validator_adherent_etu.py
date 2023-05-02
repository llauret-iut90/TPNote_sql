#! /usr/bin/python
# -*- coding:utf-8 -*-
import re
import datetime
def validator_adherent(data):
    valid = True
    errors = dict()

    if 'id_adherent' in data.keys():
        if not data['id_adherent'].isdecimal():
           errors['id_adherent'] = 'type id incorrect'
           valid= False

    if not re.match(r'\w{2,}', data['nom']):
        errors['nom'] = "Le Nom doit avoir au moins deux caractères"
        valid = False

    try:
        datetime.datetime.strptime(data['date_paiement'], '%d/%m/%Y')
    except ValueError:
        errors['date_paiement'] = "Date n'est pas valide format:%d/%m/%Y"
        valid = False
    else:
        data['date_paiement_us'] = datetime.datetime.strptime(data['date_paiement'], "%d/%m/%Y").strftime("%Y-%m-%d")
    return (valid, errors, data)