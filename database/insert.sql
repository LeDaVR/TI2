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


INSERT INTO aula(aul_ide,tipo,aul_num,aul_ava) VALUES
(1,'Aula',205,true),
(2,'Aula',105,true),
(3,'Aula',305,true);


insert into usuario values
(1,'admin','adminc',1),
(2,'doc2','con2',1),
(3,'doc3','con3',9),
(4,'doc4','con4',2),
(5,'doc5','con5',3),
(6,'doc6','con6',4),
(7,'doc7','con7',5),
(8,'doc8','con8',19),
(9,'doc9','con9',16);

insert into usuario_comun values
(2),(3),(4),(5),(6),(7),(8),(9);

insert into usuario_administrador values
(1);

update curso set cur_hor_teo = 2, cur_hora_pra = 2,  cur_hor_lab = 2 where true;
update silabo set sil_per_aca = "2020-B" WHERE true;