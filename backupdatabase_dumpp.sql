BEGIN TRANSACTION;
CREATE TABLE paziresh
                (id INTEGER PRIMARY KEY,
                arrival varchar(20) NOT NULL,
                departure varchar(20) ,
                system_input varchar(20) NOT NULL,
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
                description_moshkel varchar(200) NOT NULL);
