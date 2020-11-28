========================
REST API Documentation
========================

Services 
----------



Registrar Docente
~~~~~~~~~~~~~~~

.. code-block:: text

    /register_teacher
    
POST 
++++++

Crea un nuevo docente y retorna el docente creado.

{
	"nombre" : "Juan Carlos",
	"ape_mat" : "Zuñiga",
	"ape_pat" : "Quinto",
	"grad_aca" : "Grado academico",
	"doc_esp"  : "especialidad",
	"cat_ide" : 1,
	"dep_ide" : 1
}

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
