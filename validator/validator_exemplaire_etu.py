#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
import re
import datetime

def validator_exemplaire(data):
    valid = True
    errors = dict()
    if 'id_exemplaire' in data.keys():
        if not data['id_exemplaire'].isnumeric():
            errors['id_exemplaire'] = 'type id incorrect(numeric)'
            valid = False
    if not re.match(r'\w{2,}', data['etat']):
        errors['etat'] = "Le titre doit avoir au moins deux caractères"
        valid = False
    try:
        datetime.datetime.strptime(data['date_achat'], '%d/%m/%Y')
    except ValueError:
        errors['date_achat'] = "la Date n'est pas valide format:%d/%m/%Y"
        valid = False
    else:
        data['date_achat_iso'] = datetime.datetime.strptime(data['date_achat'], "%d/%m/%Y").strftime("%Y-%m-%d")
    try:
        float(data['prix'])
    except ValueError:
        errors['prix'] = "le Prix n'est pas valide"
        valid = False
    return (valid, errors, data)