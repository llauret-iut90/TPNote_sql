#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint

from controllers.admin_auteur import *
from controllers.admin_adherent import *
from controllers.admin_oeuvre import *
from controllers.admin_exemplaire import *
from controllers.admin_emprunt import *

from controllers.fixtures_load import *

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('admin/layout.html')



app.register_blueprint(admin_auteur)
app.register_blueprint(admin_adherent)
app.register_blueprint(admin_oeuvre)
app.register_blueprint(admin_exemplaire)
app.register_blueprint(admin_emprunt)
app.register_blueprint(fixtures_load)

if __name__ == '__main__':
    app.run()

