INSERT INTO curso(cur_ide,cur_nom) VALUES 
(1,"Ciencia de la Computacion I"),
(2,"Comunicación Integral "),
(3,"Estructuras Discretas II"),
(4,"Constitución y realidad nacional"),
(5,"Fundamentos de Computación"),
(6,"Calculo en una variable"),
(7,"Realidad Nacional"),
(8,"Ingles técnico Prof. II"),
(9," Raz. Log Matem"),
(10," Arte Computacional"),
(11," Estructuras Discretas I"),
(23,"Sistema Operativos"),
(24,"Interdisciplinar II"),
(25,"Programación Competitiva"),
(26,"EDA"),
(27,"Mat. aplicada a la computación"),
(28,"Ingeniería de Software II");


INSERT INTO silabo(sil_ide,cur_ide) VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10),
(11,11),
(23,23),
(24,24),
(25,25),
(26,26),
(27,27),
(28,28);


INSERT INTO departamento_academico(dep_ide,dep_nom) VALUES
(1,"Dep 1"),
(2,"Dep 2"),
(3,"Dep 3");

INSERT INTO categoria(cat_ide,cat_nom,hor_max,hor_min) VALUES
(1,'TP20',20,16);

INSERT INTO docente(doc_ide,doc_nom,doc_ape_mat,doc_ape_pat,dep_ide,cat_ide) VALUES
(1,"Eliana","","",1,1),
(2,"Mirian","Vera","Alcazar",2,1),
(3,"Roxana","","",3,1),
(4,"Alvaro","Mamani","Aliaga",1,1),
(5,"Erika","Lazo","Alarcon",2,1),
(6,"Ana Marìa","Alvarez","Chàvez",2,1),
(7,"Yuber","","",1,1),
(8,"Yessenia","Yari","",2,1),
(9,"Fermin","Mamani","",3,1),
(10,"Manuel","Higueras","Matos",2,1),
(11,"Gaby","Cahuana","",2,1),
(12,"Yonathan","Gonzales","Ttito",2,1),
(13,"Eliseo","Velasquez","Condori",3,1),
(14,"Marcos","Vilca","Jimenez",2,1),
(15,"Franci","Suni","",1,1),
(16,"Pablo","Calcina","Ccori",1,1),
(17,"Carlos","Atencio","",1,1),
(18,"Judith","Cruz","",3,1),
(19,"Vicente","Machaca","",1,1);

INSERT INTO grupo(gru_ide,gru_nom,sil_ide) VALUES
(1,"A",1),
(2,"A",24),
(3,"A",26);

INSERT INTO silabo_docente(sil_doc_ide,tipo_clase,horas,doc_ide,sil_ide,gru_ide) VALUES
(1,"Practica",2,1,1,1),
(2,"Teoría",2,19,24,2),
(3,"Teoría",2,19,26,3);

INSERT INTO aula(aul_ide,tipo,aul_num,aul_ava) VALUES
(1,'Aula',205,true),
(2,'Aula',105,true);

INSERT INTO horario(hor_ide,hora_entrada,hora_salida,aul_ide,sil_doc_ide,dia) VALUES
(1,"07:00:00","08:40:00",1,1,"Lunes"),
(2,"07:00:00","08:40:00",1,2,"Miercoles"),
(3,"08:50:00","10:30:00",1,3,"Miercoles");

insert into usuario values
(1,'docente1','contrasenia1',1),
(2,'docente2','contrasenia2',19);


update silabo set sil_per_aca =  1; 
update curso set cur_hor_teo = 2, cur_hora_pra = 2,  cur_hor_lab = 2;
update silabo set sil_per_aca = "2020-B";