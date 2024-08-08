CREATE DATABASE IF NOT EXISTS gestion_clients;

USE gestion_clients;

-- Table Principale
CREATE TABLE customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    salaire DECIMAL(10, 2),
    email VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table customer_deleted
CREATE TABLE customer_deleted (
    id INT,
    name VARCHAR(255),
    age INT,
    salaire DECIMAL(10, 2),
    email VARCHAR(255),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table customer_updated
CREATE TABLE customer_updated (
    id INT,
    old_name VARCHAR(255),
    old_age INT,
    old_salaire DECIMAL(10, 2),
    old_email VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tables de Réplication
CREATE TABLE customer_replication_1 LIKE customer;
CREATE TABLE customer_replication_2 LIKE customer;

-- Déclencheur pour le suivi des suppressions
DELIMITER //
CREATE TRIGGER trg_customer_delete AFTER DELETE ON customer FOR EACH ROW
BEGIN
    INSERT INTO customer_deleted (id, name, age, salaire, email)
    VALUES (OLD.id, OLD.name, OLD.age, OLD.salaire, OLD.email);
END;
//
DELIMITER ;

-- Déclencheur pour le suivi des mises à jour
DELIMITER //
CREATE TRIGGER trg_customer_update AFTER UPDATE ON customer FOR EACH ROW
BEGIN
    INSERT INTO customer_updated (id, old_name, old_age, old_salaire, old_email)
    VALUES (OLD.id, OLD.name, OLD.age, OLD.salaire, OLD.email);
END;
//
DELIMITER ;

-- Déclencheur pour la réplication en temps réel
DELIMITER //
CREATE TRIGGER trg_customer_replication_1_insert AFTER INSERT ON customer FOR EACH ROW
BEGIN
    INSERT INTO customer_replication_1 (id, name, age, salaire, email)
    VALUES (NEW.id, NEW.name, NEW.age, NEW.salaire, NEW.email);
END;
//
DELIMITER ;

-- Déclencheur pour la réplication en temps réel (mise à jour)
DELIMITER //
CREATE TRIGGER trg_customer_replication_1_update AFTER UPDATE ON customer FOR EACH ROW
BEGIN
    UPDATE customer_replication_1
    SET name = NEW.name, age = NEW.age, salaire = NEW.salaire, email = NEW.email
    WHERE id = NEW.id;
END;
//
DELIMITER ;

-- Déclencheur pour la réplication en temps réel (suppression)
DELIMITER //
CREATE TRIGGER trg_customer_replication_1_delete AFTER DELETE ON customer FOR EACH ROW
BEGIN
    DELETE FROM customer_replication_1 WHERE id = OLD.id;
END;
//
DELIMITER ;

-- Supprimer l'événement existant s'il existe déjà
DROP EVENT IF EXISTS update_replication_table;

-- Créer un nouvel événement planifié pour mettre à jour la table de réplication
CREATE EVENT IF NOT EXISTS update_replication_table
ON SCHEDULE EVERY 5 MINUTE
DO
    -- Supprimer les enregistrements existants dans customer_replication_2
    DELETE FROM customer_replication_2;
    
    -- Insérer les enregistrements mis à jour de la table customer dans customer_replication_2
    INSERT INTO customer_replication_2
    SELECT * FROM customer;