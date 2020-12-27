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
    def __init__(self,app,conexion):
        self.model = UserModel(conexion)

        @app.route('/login', methods=['POST'])
        def login():
            params = {
                'user' : request.json['user'],
                'password' : request.json['password']
            }
            return self.model.login(params)
        
        @app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('login'))
        
        @app.route('/register_user', methods=['GET', 'POST'])
        def register_user():
            params = {
                'user' : request.json['user'],
                'password' : request.json['password'],
                'doc_ide' : request.json['doc_ide']
            }
            return self.model.register(params)

