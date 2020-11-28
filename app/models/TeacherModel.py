from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class TeacherModel:

    def __init__ ( self ,app ):
        self.conexion = Conexion(app)
    
    def can_be_assigned(self, params ):

        # verificando la cantidad de horas disponibles del docente
        query = """SELECT COALESCE(SUM(HORAS),0) FROM silabo_docente 
                    WHERE doc_ide = %(doc_ide)s"""
        self.conexion.cursor.execute(query,params)
        horas_asignadas = self.conexion.cursor.fetchone()
        query = """SELECT hor_max FROM categoria c
                    WHERE cat_ide = (SELECT cat_ide FROM docente
                    WHERE doc_ide = %(doc_ide)s)"""
        self.conexion.cursor.execute(query,params)
        horas_maximas = self.conexion.cursor.fetchone()

        # verificando horas del curso
        query = """
                SELECT COALESCE(SUM(horas),0) FROM silabo_docente
                WHERE gru_ide = %(gru_ide)s 
                AND tipo_clase = %(tipo_clase)s
                AND sil_ide = %(sil_ide)s
                """
        self.conexion.cursor.execute(query,params)
        hor_cur_asi = self.conexion.cursor.fetchone()[0]
        tipo = ""
        if params['tipo_clase'] == "Teoría":
            tipo = "cur_hor_teo"
        if params['tipo_clase']  == "Practica":
            tipo = "cur_hora_pra"
        if params['tipo_clase'] == "Laboratorio":
            tipo = "cur_hor_lab"
        
        query = """
                SELECT """ + tipo  +  """ FROM curso
                WHERE cur_ide = (
                    SELECT cur_ide FROM silabo
                    WHERE sil_ide = %(sil_ide)s
                )
                """
        self.conexion.cursor.execute(query,params)
        hor_cur_tot = self.conexion.cursor.fetchone()[0]

        print(hor_cur_asi,hor_cur_tot)
        if horas_asignadas[0] + params['horas'] <= horas_maximas[0]:
            if hor_cur_asi + params['horas'] <= hor_cur_tot:
                return True
        return False

    def assign_teacher(self , params):

        query = """INSERT INTO silabo_docente(tipo_clase,horas,doc_ide,sil_ide,gru_ide) VALUES
                    (%(tipo_clase)s,%(horas)s,%(doc_ide)s,%(sil_ide)s,%(gru_ide)s)"""
        self.conexion.cursor.execute(query,params)
        self.conexion.conn.commit()

        data = {
            'sil_doc_ide' : self.conexion.cursor.lastrowid , 
            'tipo_clase' : params['tipo_clase'],
            'horas' : params['horas'],
            'gru_ide' : params['gru_ide'],
            'doc_ide' : params['doc_ide'],
            'sil_ide' : params['sil_ide']
        }
        return data
    
    def unassign(self , params):

        query = """
                DELETE FROM silabo_docente
                WHERE sil_doc_ide = %(sil_doc_ide)s
                """
        self.conexion.cursor.execute(query,params)
        self.conexion.conn.commit()

        data = {
            'sil_doc_ide' : params['sil_doc_ide']
        }
        return data


    def register(self, params):
        query = """ insert into docente(doc_nom, doc_ape_mat, doc_ape_pat, doc_grad_aca,
        doc_esp, cat_ide, dep_ide) values (%(nombre)s, %(ape_mat)s, %(ape_pat)s, %(grad_aca)s,
        %(esp)s, %(cat_ide)s, %(dep_ide)s);"""
        self.conexion.cursor.execute(query, params)
        self.conexion.conn.commit()

        data = {
            'doc_ide' : self.conexion.cursor.lastrowid , 
            'doc_nom' : params['nombre'],
            'doc_ape_mat' : params['ape_mat'],
            'doc_ape_pat' : params['ape_pat'],
            'doc_grad_aca' : params['grad_aca'],
            'doc_esp' : params['esp'],
            'cat_ide' : params['cat_ide'],
            'dep_ide' : params['dep_ide']
        }
        return jsonify(data)


    def teacher_schedule(self,params):
        query = """
                SELECT  sd.tipo_clase as "tipo clase",
                        g.gru_nom as "grupo",
                        h.hora_entrada as "hora entrada",
                        h.hora_salida as "hora salida",
                        h.aul_ide as "aula",
                        h.dia as "dia"
                FROM silabo_docente sd
                LEFT JOIN grupo g
                on sd.gru_ide = g.gru_ide
                LEFT JOIN horario h
                on sd.sil_doc_ide = h.sil_doc_ide
                WHERE sd.doc_ide = %(id)s
                """
        self.conexion.cursor.execute(query,params)
        rv = self.conexion.cursor.fetchall()
        data_names = data_names = self.conexion.cursor.description
        print(rv)
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        return jsonify(data)
    
    def register(self, params):
        query = """ insert into docente(doc_nom, doc_ape_mat, doc_ape_pat, doc_grad_aca,
        doc_esp, cat_ide, dep_ide) values (%(nombre)s, %(ape_mat)s, %(ape_pat)s, %(grad_aca)s,
        %(doc_esp)s, %(cat_ide)s, %(dep_ide)s);"""
        self.conexion.cursor.execute(query, params)
        self.conexion.conn.commit()

        data = {
            'doc_ide' : self.conexion.cursor.lastrowid , 
            'doc_nom' : params['nombre'],
            'doc_ape_mat' : params['ape_mat'],
            'doc_ape_pat' : params['ape_pat'],
            'doc_grad_aca' : params['grad_aca'],
            'doc_esp' : params['doc_esp'],
            'cat_ide' : params['cat_ide'],
            'dep_ide' : params['dep_ide']
        }
        return jsonify(data)