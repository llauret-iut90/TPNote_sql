#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
def validator_auteur(data):
    valid = True
    errors = dict()
    if not re.match(r'\w{2,}', data['nom']):
        # flash('Nom doit avoir au moins deux caractères')
        errors['nom'] = 'Nom doit avoir au moins deux caractères'
        valid = False
    if 'id_auteur' in data.keys():
        if not data['id_auteur'].isdecimal():
            errors['id_auteur'] = 'type id incorrect'
            valid = False
    return (valid, errors)