drop database construction;
create database construction;
use construction;

CREATE TABLE IF NOT EXISTS projects(
    p_id int PRIMARY KEY,
    p_name varchar(20),
    budget int,
    mgr_ssn int,
    st_date date,
    expected_finish date

);

CREATE TABLE IF NOT EXISTS employee(
    emp_ssn int PRIMARY KEY,
    emp_name varchar(20),
    contact bigint,
    p_id int,
    Roles varchar(20),
    psword varchar(100),
    FOREIGN KEY (p_id) REFERENCES projects(p_id) ON DELETE SET NULL

);

ALTER TABLE projects ADD FOREIGN KEY (mgr_ssn) REFERENCES employee(emp_ssn) ON DELETE SET NULL ;

CREATE TABLE IF NOT EXISTS client(
    client_id int PRIMARY KEY,
    client_name varchar(20),
    contact bigint,
    p_id int DEFAULT NULL,
    pin int,
    sta varchar(20),
    locality varchar(100),
    FOREIGN KEY (p_id) REFERENCES projects(p_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS site_(
    site_id int PRIMARY KEY,
    mgr_ssn int,
    site_name varchar(100),
    addr varchar(200),
    p_id int,
    registration_office varchar(100),
    FOREIGN KEY (mgr_ssn) REFERENCES employee(emp_ssn) ON DELETE SET NULL,
    FOREIGN KEY (p_id) REFERENCES projects(p_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS materials(
    material_id int PRIMARY KEY,
    material_name varchar(100),
    p_id int,
    descript varchar(150),
    Quantity varchar(10),
    FOREIGN KEY (p_id) REFERENCES projects(p_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS legal_docs(
    registration int,
    site_id int,
    land_type varchar(20),
    descript varchar(100),
    acquired_under varchar(20),
    doc varchar(100),
    FOREIGN KEY (site_id) REFERENCES site_(site_id)
);

CREATE TABLE IF NOT EXISTS reports(
    p_id int,
    report varchar(200),
    emp_ssn int
);


CREATE TABLE IF NOT EXISTS machinery(
    m_name varchar(30),
    m_desc varchar(30),
    str date,
    stp date
);


DELIMITER //
CREATE PROCEDURE select_all_sites()
BEGIN
    SELECT * FROM site_;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE select_all_project_ids()
BEGIN
    SELECT p_id FROM projects;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER project_delete_trigger
AFTER DELETE ON projects
FOR EACH ROW
BEGIN
    UPDATE employee SET p_id = NULL WHERE p_id = OLD.p_id;
    UPDATE client SET p_id = NULL WHERE p_id = OLD.p_id;    
    DELETE FROM site_ WHERE p_id = OLD.p_id;
    DELETE FROM materials WHERE p_id = OLD.p_id;
END;
//
DELIMITER ;

DELIMITER //

CREATE TRIGGER update_projects_mgr_ssn
AFTER UPDATE ON site_
FOR EACH ROW
BEGIN
    DECLARE projects_mgr_ssn INT;

    SELECT mgr_ssn INTO projects_mgr_ssn
    FROM projects
    WHERE p_id = NEW.p_id;

    IF projects_mgr_ssn = NEW.mgr_ssn THEN
        UPDATE projects
        SET mgr_ssn = NULL
        WHERE p_id = NEW.p_id;
    END IF;
END //

DELIMITER ;
