-- =========================================================================
--             SCRIPT DE STRUCTURE SQL (DDL) - PROJET CALAL
--     Représentation du schéma relationnel MySQL (Moteur InnoDB)
-- =========================================================================

CREATE DATABASE IF NOT EXISTS calal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE calal_db;

-- -------------------------------------------------------------------------
-- 1. Table: users_customuser (Table centrale des utilisateurs & biometrie)
-- -------------------------------------------------------------------------
CREATE TABLE `users_customuser` (
    `id` INT AUTO_INCREMENT NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME NULL,
    `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
    `username` VARCHAR(150) NOT NULL UNIQUE,
    `first_name` VARCHAR(150) NOT NULL,
    `last_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(254) NOT NULL UNIQUE,
    `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `date_joined` DATETIME NOT NULL,
    `name` VARCHAR(100) NULL,
    `age` INT NULL,
    `gender` VARCHAR(10) NULL,
    `height` DOUBLE NULL,
    `weight` DOUBLE NULL,
    `goal` VARCHAR(10) NULL,
    `activity_level` VARCHAR(20) NULL,
    
    PRIMARY KEY (`id`) -- Clé Primaire unique
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------------
-- 2. Table: nutrition_meal (Journal des repas consommes par l'utilisateur)
-- -------------------------------------------------------------------------
CREATE TABLE `nutrition_meal` (
    `id` INT AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `calories` INT NOT NULL,
    `protein` DOUBLE NOT NULL DEFAULT 0.0,
    `carbs` DOUBLE NOT NULL DEFAULT 0.0,
    `fat` DOUBLE NOT NULL DEFAULT 0.0,
    `meal_type` VARCHAR(50) NOT NULL,
    `date` DATE NOT NULL,
    `user_id` INT NOT NULL,
    
    PRIMARY KEY (`id`), -- Clé Primaire du repas
    
    -- Clé Étrangère reliant le repas à l'utilisateur
    CONSTRAINT `fk_nutrition_meal_user` 
        FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE -- Suppression en cascade (RGPD)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------------
-- 3. Table: workouts_workout (Catalogue de references des exercices)
-- -------------------------------------------------------------------------
CREATE TABLE `workouts_workout` (
    `id` INT AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `duration_minutes` INT NOT NULL,
    `calories_burned` INT NOT NULL,
    
    PRIMARY KEY (`id`) -- Clé Primaire du workout de base
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------------
-- 4. Table: workouts_userworkout (Historique de sport effectue par l'athlete)
-- -------------------------------------------------------------------------
CREATE TABLE `workouts_userworkout` (
    `id` INT AUTO_INCREMENT NOT NULL,
    `date` DATE NOT NULL,
    `duration` INT NOT NULL,
    `user_id` INT NOT NULL,
    `workout_id` INT NOT NULL,
    
    PRIMARY KEY (`id`), -- Clé Primaire de la ligne d'historique
    
    -- Clé Étrangère reliant la séance à l'utilisateur
    CONSTRAINT `fk_workouts_userworkout_user` 
        FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE,
        
    -- Clé Étrangère reliant la séance à la fiche du catalogue
    CONSTRAINT `fk_workouts_userworkout_workout` 
        FOREIGN KEY (`workout_id`) REFERENCES `workouts_workout` (`id`) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------------------
-- INDEX DE PERFORMANCE (Pour accelerer les requetes de jointure dans Django)
-- -------------------------------------------------------------------------
CREATE INDEX `idx_nutrition_meal_user_date` ON `nutrition_meal` (`user_id`, `date`);
CREATE INDEX `idx_workouts_userworkout_user_date` ON `workouts_userworkout` (`user_id`, `date`);
