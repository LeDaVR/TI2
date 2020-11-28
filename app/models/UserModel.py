from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class UserModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    
    def login(self , params ) :
        query = """
                SELECT * FROM usuario 
                WHERE usu_user = %(user)s and usu_pass = %(password)s 
                """
        self.conexion.cursor.execute(query,params)
        data_names = self.conexion.cursor.description
        rv = self.conexion.cursor.fetchone()
        if rv is None:
            data = None
        else:
            data = {}
            for i in range(len(rv)):
                data[data_names[i][0]] = rv[i]

        return jsonify(data)

    def register(self, params):
        query = """ insert into usuario(usu_user, usu_pass, doc_ide)
        values (%(user)s, %(password)s, %(doc_ide)s);"""
        self.conexion.cursor.execute(query, params)
        self.conexion.conn.commit()

        data = {
            'usu_ide' : self.conexion.cursor.lastrowid , 
            'usu_user' : params['user'],
            'usu_pass' : params['password'],
            'doc_ide' : params['doc_ide']
        }
        return jsonify(data)