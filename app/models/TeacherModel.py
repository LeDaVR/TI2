from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class TeacherModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    
    def can_be_assigned(self,doc_ide,horas):
        params = {
            'doc_ide' : doc_ide,
            'horas' : horas,
        }
        query = """SELECT SUM(HORAS) FROM silabo_docente 
                    WHERE doc_ide = %(doc_ide)s"""
        self.conexion.cursor.execute(query,params)
        horas_asignadas = self.conexion.cursor.fetchone()
        query = """SELECT hor_max FROM categoria c
                    WHERE cat_ide = (SELECT cat_ide FROM docente
                    WHERE doc_ide = %(doc_ide)s)"""
        self.conexion.cursor.execute(query,params)
        horas_maximas = self.conexion.cursor.fetchone()
        if horas_asignadas[0] + horas <= horas_maximas[0]:
            return True
        return False

    def assign_teacher(self ,tipo_clase, horas, gru_ide, doc_ide, sil_ide ):
        params = {
            'tipo_clase' : tipo_clase,
            'horas' : horas,
            'gru_ide' : gru_ide,
            'doc_ide' : doc_ide,
            'sil_ide' : sil_ide
        }
        query = """INSERT INTO silabo_docente(tipo_clase,horas,doc_ide,sil_ide,gru_ide) VALUES
                    (%(tipo_clase)s,%(horas)s,%(doc_ide)s,%(sil_ide)s,%(gru_ide)s)"""
        self.conexion.cursor.execute(query,params)
        self.conexion.conn.commit()

        data = {
            'sil_doc_ide' : self.conexion.cursor.lastrowid , 
            'tipo_clase' : tipo_clase,
            'horas' : horas,
            'gru_ide' : gru_ide,
            'doc_ide' : doc_ide,
            'sil_ide' : sil_ide
        }
        return data



