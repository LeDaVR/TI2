
========================
REST API Documentation
========================


Registrar Docente
----------


Permite registar un docente en la base de datos

.. code-block:: text
	
	/register_teacher



POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
nombre           Nombre del docente
ape_mat          Apellido materno del docente
ape_pat          Apellido materno del docente
grad_aca         Grado academico del docente
doc_esp          Especialidad del docente
cat_ide          Identificador de la categoria del docente
dep_ide          Identificador del departamento académico
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

        {
		"nombre" : "Juan Carlos",
		"ape_mat" : "Zuñiga",
		"ape_pat" : "Quinto",
		"grad_aca" : "Grado academico",
		"doc_esp"  : "especialidad",
		"cat_ide" : 1,
		"dep_ide" : 1
        }


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

        {
		"cat_ide": 1,
		"dep_ide": 1,
		"doc_ape_mat": "Zuñiga",
		"doc_ape_pat": "Quinto",
		"doc_esp": "especialidad",
		"doc_grad_aca": "Grado academico",
		"doc_ide": 20,
		"doc_nom": "Juan Carlos"
        }


Asignar Docente
----------


Asigna a un docente una cantida de horas en una asignatura.

.. code-block:: text
	
	/assign_teacher



POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
doc_ide          Identificador del docente
sil_ide          Identificador del sílabo
gru_ide          Identificador del grupo 
tipo_clase       Tipo de clase(Teoría,Laboratorio,Práctica)
horas            Cantidad de horas 
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

        {
		"doc_ide" : 1 ,
		"sil_ide" : 1,
		"gru_ide" : 1,
		"tipo_clase" : "Teoría",
		"horas" : 2
	}


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

        {
		"doc_ide": 1,
		"gru_ide": 1,
		"horas": 2,
		"sil_doc_ide": 5,
		"sil_ide": 1,
		"tipo_clase": "Teoría"
	}
	

Desasignar docente
----------

Elimina las horas asignadas de un docente, también elimina el horario correspondiente a estas horas.

.. code-block:: text
	
	/unassign_teacher



POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
sil_doc_ide      Identificador de las horas asignadas
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

        {
		"sil_doc_ide" : 2
	}


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

        {
  		"sil_doc_ide": 2
	}

Horario de docente
----------

Muestra el horario del docente en formato json.

.. code-block:: text
	
	/teacher_schedule/{id}



POST 
+++++++++++


==============   ===============
Property         Description
==============   ===============
id	         Identificador del docente
==============   ===============



RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

        [
		{
			"aula": "1",
			"dia": "Lunes",
			"grupo": "A",
			"hora entrada": "7:00:00",
			"hora salida": "8:40:00",
			"tipo clase": "Practica"
		}
	]

CREAR GRUPOS
----------

Crea grupos para el semestre actual en orden alfabetico.

.. code-block:: text
	
	/create_group


POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
cantidad         Cantidad de grupos a crear.
sil_ide          Identificador del sílabo actual del curso.
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

        {
		"cantidad" : 3,
		"sil_ide" : 27
	}


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

	[
		  {
		    "gru_ide": 9,
		    "gru_nom": "A",
		    "gru_tur": "Mañana",
		    "sil_ide": 27
		  },
		  {
		    "gru_ide": 10,
		    "gru_nom": "B",
		    "gru_tur": "Tarde",
		    "sil_ide": 27
		  },
		  {
		    "gru_ide": 11,
		    "gru_nom": "C",
		    "gru_tur": "Mañana",
		    "sil_ide": 27
		  }
	]


REGISTRAR USUARIO
----------

Crea un usuario para un docente registrado.

.. code-block:: text
	
	/register_user


POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
user             Nombre de usuario.
password         Contraseña del usuario.
doc_ide          Identificador del docente.
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

	{
		"user" : "docente3",
		"password" : "contrasenia3",
		"doc_ide" : 20
	}


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

        {
	  "doc_ide": 20,
	  "usu_ide": 3,
	  "usu_pass": "contrasenia3",
	  "usu_user": "docente3"
	}


CREAR HORARIO
----------

Registra un horario de las horas asignadas a un docente en una asignatura.

.. code-block:: text
	
	/create_schedule


POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
hora_entrada     Hora de entrada.
hora_salida      Hora de salida.
aul_ide          Identificador del aula.
dia		 Dia de la clase
sil_doc_ide      Identificador de las horas asignadas
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

	{
		"hora_entrada" : "10:40:00" ,
		"hora_salida" : "12:20:00", 
		"aul_ide" : 2, 
		"dia" : "Miercoles" ,
		"sil_doc_ide" : 5
	}


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

	{
	  "aul_ide": 2,
	  "dia": "Miercoles",
	  "hor_ide": 8,
	  "hora_entrada": "10:40:00",
	  "hora_salida": "12:20:00",
	  "sil_doc_ide": 5
	}

OBTENER HORARIO
----------

Devuelve el horario completo de un semestre.

.. code-block:: text
	
	/get_schedule/{per_aca}


POST 
+++++++++++


==============   ===============
Property            Description
==============   ===============
per_aca     	 Periodo Académico
==============   ===============


RESPONSE
~~~~~~~~~~~~~~~

.. code-block:: js

	[
	  {
	    "aula": "1",
	    "dia": "Lunes",
	    "grupo": "A",
	    "hora entrada": "7:00:00",
	    "hora salida": "8:40:00",
	    "tipo clase": "Practica"
	  },
	  {
	    "aula": "1",
	    "dia": "Miercoles",
	    "grupo": "A",
	    "hora entrada": "7:00:00",
	    "hora salida": "8:40:00",
	    "tipo clase": "Teoría"
	  },
	  {
	    "aula": "1",
	    "dia": "Miercoles",
	    "grupo": "A",
	    "hora entrada": "8:50:00",
	    "hora salida": "10:30:00",
	    "tipo clase": "Teoría"
	  }
	]



BORRAR HORARIO
----------

Elimina el horario de una clase asignada a un docente.

.. code-block:: text
	
	/delete_schedule


POST 
+++++++++++


==============   ===============
Param            Description
==============   ===============
hor_ide		 Identificador del horario
==============   ===============

REQUEST
~~~~~~~~~~~~~~~


.. code-block:: js

	{
		"hor_ide" : 3
	}

