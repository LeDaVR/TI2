from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class UserModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    
    def login(self , usu_user ) :
        self.conexion.cursor.execute("SELECT * from usuario where usu_user='"+usu_user+"';" )
        data_names = self.conexion.cursor.description
        rv = self.conexion.cursor.fetchone()
        if rv is None:
            data = None
        else:
            data = {}
            for i in range(len(rv)):
                data[data_names[i][0]] = rv[i]

        print(data)
        return data