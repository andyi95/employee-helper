-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "password_hash" VARCHAR(128),
    "last_login" TIMESTAMP,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "employer" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL  DEFAULT '',
    "url" VARCHAR(255) NOT NULL  DEFAULT ''
);
CREATE TABLE IF NOT EXISTS "skill" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "vacancy" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL  DEFAULT '',
    "salary_defined" BOOL NOT NULL  DEFAULT False,
    "salary_from" INT,
    "salary_to" INT,
    "schedule" VARCHAR(512) NOT NULL  DEFAULT '',
    "description" TEXT NOT NULL,
    "published_at" TIMESTAMP NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "remote" BOOL NOT NULL  DEFAULT False,
    "expierence" VARCHAR(18) NOT NULL  DEFAULT 'Нет опыта',
    "address" TEXT NOT NULL,
    "lat" VARCHAR(16) NOT NULL  DEFAULT '',
    "lon" VARCHAR(16) NOT NULL  DEFAULT '',
    "employer_id" BIGINT REFERENCES "employer" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "vacancy"."expierence" IS 'noExpierence: Нет опыта\nbetween1And3: От 1 года до 3 лет';
CREATE TABLE IF NOT EXISTS "vacancyskill" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "skill_id" BIGINT REFERENCES "skill" ("id") ON DELETE SET NULL,
    "vacancy_id" BIGINT REFERENCES "vacancy" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
