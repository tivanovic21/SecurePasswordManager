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
    "first_name" VARCHAR(45),
    "last_name" VARCHAR(45),
    "twoFA" BOOLEAN,
    "twoFA_secret" VARCHAR(100),
    CONSTRAINT "id_UNIQUE" UNIQUE("id"),
    CONSTRAINT "username_UNIQUE" UNIQUE("email")
);
CREATE TABLE "Websites"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(45),
    "domain" VARCHAR(45),
    "User_id" INTEGER NOT NULL,
    CONSTRAINT "fk_Websites_User" FOREIGN KEY("User_id") REFERENCES "User"("id")
);
CREATE INDEX "Websites.fk_Websites_User_idx" ON "Websites" ("User_id");
CREATE TABLE "Password"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "password" VARCHAR(1000) NOT NULL,
    "User_id" INTEGER NOT NULL,
    "Websites_id" INTEGER NOT NULL,
    CONSTRAINT "fk_Password_User1" FOREIGN KEY("User_id") REFERENCES "User"("id"),
    CONSTRAINT "fk_Password_Websites1" FOREIGN KEY("Websites_id") REFERENCES "Websites"("id")
);
CREATE INDEX "Password.fk_Password_User1_idx" ON "Password" ("User_id");
CREATE INDEX "Password.fk_Password_Websites1_idx" ON "Password" ("Websites_id");
COMMIT;