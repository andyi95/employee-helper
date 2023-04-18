-- upgrade --
CREATE TABLE IF NOT EXISTS "profrole" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);;
CREATE TABLE IF NOT EXISTS "vacancyprofrole" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "vacancy_id" BIGINT REFERENCES "vacancy" ("id") ON DELETE CASCADE,
    "role_id" BIGINT REFERENCES "profrole" ("id") ON DELETE CASCADE
);-- downgrade --
DROP TABLE IF EXISTS "profrole";
DROP TABLE IF EXISTS "vacancyprofrole";
