BEGIN TRANSACTION;
CREATE TABLE q1_person_name
                 (name_id INTEGER PRIMARY KEY,
                  first_name varchar(20) NOT NULL,
                  last_name varchar(20) NOT NULL);
INSERT INTO "q1_person_name" VALUES(1,'Michael','Fox');
INSERT INTO "q1_person_name" VALUES(2,'Adam','Miller');
INSERT INTO "q1_person_name" VALUES(3,'Andrew','Peck');
INSERT INTO "q1_person_name" VALUES(4,'James','Shroyer');
INSERT INTO "q1_person_name" VALUES(5,'Eric','Burger');
INSERT INTO "q1_person_name" VALUES(6,'amir','attary');
INSERT INTO "q1_person_name" VALUES(7,'amirr','attary');
INSERT INTO "q1_person_name" VALUES(8,'amirr','attary');
INSERT INTO "q1_person_name" VALUES(9,'amirrr','attary');
INSERT INTO "q1_person_name" VALUES(10,'amirrr','attary');
INSERT INTO "q1_person_name" VALUES(11,'amirrr','attary');
INSERT INTO "q1_person_name" VALUES(12,'amirrr','attary');
INSERT INTO "q1_person_name" VALUES(13,'amirrr','attary');
COMMIT;
