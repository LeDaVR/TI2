from flask import Flask
from flask import request
from flask import jsonify
from flask import flash
from flaskext.mysql import MySQL
from models import UserModel
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import click
from flask.cli import with_appcontext

class UserController:
    def __init__(self,app):
        self.model = UserModel(app)

        @app.route('/login', methods=['POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                error = None
                user = self.model.login(username)
                if user is None:
                    error = 'Incorrect username.'
                elif not user['usu_pass'] ==  password:
                    error = 'Incorrect password.'

                if error is None:
                    session.clear()
                    session['user_id'] = user['doc_ide']
                    return redirect(url_for('edit'))
                
                flash(error)

            return render_template('login.html')
        
        @app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('login'))
        
        @app.route('/register_user',methods=['POST'])
        def register_user():
            return 1

