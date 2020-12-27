from flask import jsonify
from flaskext.mysql import MySQL
from .conexion import Conexion

class TeacherModel:

    def __init__ ( self ,conexion ):
        self.conexion = conexion
    
    def can_be_assigned(self, params ):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        # verificando la cantidad de horas disponibles del docente
        query = """SELECT COALESCE(SUM(HORAS),0) FROM silabo_docente 
                    WHERE doc_ide = %(doc_ide)s"""
        cursor.execute(query,params)
        horas_asignadas = cursor.fetchone()
        query = """SELECT hor_max FROM categoria c
                    WHERE cat_ide = (SELECT cat_ide FROM docente
                    WHERE doc_ide = %(doc_ide)s)"""
        cursor.execute(query,params)
        horas_maximas = cursor.fetchone()

        # verificando horas del curso
        query = """
                SELECT COALESCE(SUM(horas),0) FROM silabo_docente
                WHERE gru_ide = %(gru_ide)s 
                AND tipo_clase = %(tipo_clase)s
                AND sil_ide = %(sil_ide)s
                """
        cursor.execute(query,params)
        hor_cur_asi = cursor.fetchone()[0]
        tipo = ""
        if params['tipo_clase'] == "Teoría":
            tipo = "cur_hor_teo"
        if params['tipo_clase']  == "Práctica":
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
        cursor.execute(query,params)
        hor_cur_tot = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        print(hor_cur_asi,hor_cur_tot)
        if horas_asignadas[0] + params['horas'] <= horas_maximas[0]:
            if hor_cur_asi + params['horas'] <= hor_cur_tot:
                return True
        return False

    def assign_teacher(self , params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """INSERT INTO silabo_docente(tipo_clase,horas,doc_ide,sil_ide,gru_ide) VALUES
                    (%(tipo_clase)s,%(horas)s,%(doc_ide)s,%(sil_ide)s,%(gru_ide)s)"""
        cursor.execute(query,params)
        conn.commit()


        data = {
            'sil_doc_ide' : cursor.lastrowid , 
            'tipo_clase' : params['tipo_clase'],
            'horas' : params['horas'],
            'gru_ide' : params['gru_ide'],
            'doc_ide' : params['doc_ide'],
            'sil_ide' : params['sil_ide']
        }
        cursor.close()
        conn.close()
        return data
    
    def unassign(self , params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                DELETE FROM silabo_docente
                WHERE sil_doc_ide = %(sil_doc_ide)s
                """
        cursor.execute(query,params)
        conn.commit()

        data = {
            'sil_doc_ide' : params['sil_doc_ide']
        }
        cursor.close()
        conn.close()
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


    def schedule_to_chose(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT  sd.sil_doc_ide as sil_doc, 
                        c.cur_nom as "asignatura",
                        sd.tipo_clase as "tipo_clase",
                        g.gru_nom as "grupo",
                        h.horas
                FROM silabo_docente sd
                INNER JOIN grupo g
                on sd.gru_ide = g.gru_ide
                INNER JOIN silabo s
                ON s.sil_ide = sd.sil_ide
                INNER JOIN curso c
                ON c.cur_ide = s.cur_ide
                LEFT JOIN (select sil_doc_ide,COUNT(hor_ide) as horas FROM horario GROUP BY sil_doc_ide) h
                ON h.sil_doc_ide = sd.sil_doc_ide
                WHERE sd.doc_ide = %(id)s and sd.horas > coalesce(h.horas,0)
                """
        cursor.execute(query,params)
        rv = cursor.fetchall()
        data_names = data_names = cursor.description
        print(rv)
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        cursor.close()
        conn.close()
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

    def teachers(self):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT doc_ide as ID , CONCAT(doc_nom,' ',doc_ape_mat,' ',doc_ape_pat) AS Nombre FROM docente; 
                """
        cursor.execute(query)
        rv = cursor.fetchall()
        data_names = data_names = cursor.description
        if rv is None:
            data = None
        else:
            data = [] 
            for i in range(len(rv)):
                data.append({})
                for j in range(len(rv[i])):
                    (data[i])[data_names[j][0]] = str(rv[i][j]) 
        cursor.close()
        conn.close()
        return jsonify(data)
    
    def teacher_info(self,params):
        conn = self.conexion.getConexion()
        cursor = conn.cursor()
        query = """
                SELECT d.doc_ide as ID , CONCAT(doc_nom,' ',doc_ape_mat,' ',doc_ape_pat) AS nombre,
                        d.doc_grad_aca ,d.doc_esp,c.cat_nom,COALESCE(SUM(s.horas),0) as hor_asi 
                FROM docente d
                INNER JOIN silabo_docente s
                ON d.doc_ide = s.doc_ide
                INNER JOIN categoria c
                ON d.cat_ide = c.cat_ide
                WHERE d.doc_ide = %(id)s; 
                """
        cursor.execute(query,params)
        rv = cursor.fetchone()
        data_names = data_names = cursor.description

        if rv is None:
            data = None
        else:
            data = {}
            for i in range(len(rv)):
                    data[data_names[i][0]] = str(rv[i]) 
        cursor.close()
        conn.close()
        return jsonify(data)
    
    def teacher_signature(self,params):
        query = """
                select g.gru_nom as grupo , COALESCE(l.horas,0) as laboratorio, COALESCE(p.horas,0) as practica , COALESCE(t.horas,0) as teoria
                from grupo g
                left join ( select gru_ide,sum(horas) as  horas from silabo_docente 
                where tipo_clase = "Laboratorio" and doc_ide = %(doc_ide)s) l
                on  l.gru_ide = g.gru_ide
                left join ( select gru_ide,sum(horas) as  horas from silabo_docente 
                where tipo_clase = "Practica" and doc_ide = %(doc_ide)s) p
                on  p.gru_ide = g.gru_ide
                left join ( select gru_ide,sum(horas) as  horas from silabo_docente 
                where tipo_clase = "Teoria" and doc_ide = %(doc_ide)s) t
                on  t.gru_ide = g.gru_ide
                where g.sil_ide = %(sil_ide)s order by g.gru_ide;
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
        print(data)
        return jsonify(data)

