from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class UserModel:

    def __init__ ( self ,conexion ):
        self.conexion = conexion
    
    def login(self , params ) :
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                select u.usu_ide,u.doc_ide,u.usu_user,u.usu_pass, a.usu_ide as admin  from usuario u
                left join usuario_administrador a
                on a.usu_ide = u.usu_ide
                where u.usu_user = %(user)s and u.usu_pass = %(password)s ;
                """
        cursor.execute(query,params)
        data_names = cursor.description
        rv = cursor.fetchone()
        data = {}
        for i in range(len(data_names)):
            data[data_names[i][0]] =  "None"

        if rv is None:
            rv = []
        
        for i in range(len(rv)):
            data[data_names[i][0]] = rv[i]

        print(data)
        cursor.close()
        conn.close()
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