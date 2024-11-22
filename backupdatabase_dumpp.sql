BEGIN TRANSACTION;
CREATE TABLE paziresh
                (id INTEGER PRIMARY KEY,
                arrival varchar(20) NOT NULL,
                departure varchar(20) ,
                system varchar(20) NOT NULL,
                system_type varchar(20) NOT NULL,
                system_model varchar(20) NOT NULL,
                system_serial INTEGER(20) NOT NULL,
                input_name varchar(20) NOT NULL,
                tel INTEGER(10) NOT NULL,
                code_meli INTEGER(11) NOT NULL,
                tel_sabet INTEGER(10) ,
                adress varchar(200) NOT NULL,
                problem varchar(20) NOT NULL,
                cost INTEGER(100) ,
                description varchar(200) NOT NULL);
INSERT INTO "paziresh" VALUES(1,'1403/09/02','1403/09/02','ديجيتال','PLOSMA','mod-15',15545,'اميررضا عطاري ',9159526624,781183618,5144428081,'استان

','گي',50000,'شکستگی

');
INSERT INTO "paziresh" VALUES(2,'1403/09/02','','dgdg','LCD','dgdfgd',6454,'dfgdfg',59849,694165,641955,'استان

','dgdfgdf','','شکستگی

');
INSERT INTO "paziresh" VALUES(3,'1403/09/02','','sdfsdf','LCD','sdfgsag',978478,'sdfsdafag',416513,96469,89463,'استان

','gfasdgas','','شکستگی

');
INSERT INTO "paziresh" VALUES(4,'1403/09/02','','dfgdg','LCD','sdfdsfsd',69416,'sdfsdfsagd',4896451,684165,6549865,'استان

','sdfsdf','','شکستگی

');
INSERT INTO "paziresh" VALUES(5,'1403/09/02','','','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(6,'1403/09/02','','sdfsdf','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(7,'1403/09/02','','sadf','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(8,'1403/09/02','','سبشيب','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(9,'1403/09/02','','sfsdf','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(10,'1403/09/02','','sdfs','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(11,'1403/09/02','','gfdg','LCD','','','','','','','استان

','','','شکستگی

');
INSERT INTO "paziresh" VALUES(12,'1403/09/02','','asdfd','LCD','sdfsdf',65146,'sdfsdf',9159526624,781183618,5144428081,'استان','dfsdf',50000,'شکستگی');
INSERT INTO "paziresh" VALUES(13,'1403/09/02','','asdfd','LCD','sdfsdf',65146,'sdfsdf',9159526624,781183618,5144428081,'استان','dfsdf',50000,'شکستگی');
INSERT INTO "paziresh" VALUES(14,'1403/09/02','','asfdsa','LCD','asfsdf',5651,'sdfsadfsa',9330570810,790430289,5144412141,'استان','sdfasdfsad',60000,'شکستگی');
INSERT INTO "paziresh" VALUES(15,'1403/09/02','','gsgr','LCD','sdfgdfsg',9640,'dsgfdfg',9353256332,781156619,5144428400,'استان','afgagag',6000,'شکستگی');
COMMIT;
