-- Creator:       MySQL Workbench 8.0.34/ExportSQLite Plugin 0.1.0
-- Author:        38597
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2024-04-15 21:59
-- Created:       2024-04-15 21:59
BEGIN;
CREATE TABLE "User"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" VARCHAR(45) NOT NULL,
    "master_password" VARCHAR(45) NOT NULL,
    "username" VARCHAR(100),
    "twoFA" BOOLEAN,
    "twoFA_secret" VARCHAR(100),
    "fingerprint" BOOLEAN,
    "token" VARCHAR(100),
    "token_expiration" DATETIME,
    CONSTRAINT "id_UNIQUE" UNIQUE("id"),
    CONSTRAINT "username_UNIQUE" UNIQUE("email")
);
CREATE TABLE "Application"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "app_name" VARCHAR(45),
    "domain" VARCHAR(45),
    "User_id" INTEGER NOT NULL,
    CONSTRAINT "fk_Application_User" FOREIGN KEY("User_id") REFERENCES "User"("id")
);
CREATE INDEX "Application.fk_Application_User_idx" ON "Application" ("User_id");
CREATE TABLE "Password"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(100) NOT NULL,
    "password" VARCHAR(1000) NOT NULL,
    "User_id" INTEGER NOT NULL,
    "Application_id" INTEGER NOT NULL,
    CONSTRAINT "fk_Password_User1" FOREIGN KEY("User_id") REFERENCES "User"("id"),
    CONSTRAINT "fk_Password_Application1" FOREIGN KEY("Application_id") REFERENCES "Application"("id")
);
CREATE INDEX "Password.fk_Password_User1_idx" ON "Password" ("User_id");
CREATE INDEX "Password.fk_Password_Application1_idx" ON "Password" ("Application_id");
COMMIT;