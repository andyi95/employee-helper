-- upgrade --
ALTER TABLE "vacancy" ALTER COLUMN "address" SET DEFAULT '';
-- downgrade --
ALTER TABLE "vacancy" ALTER COLUMN "address" DROP DEFAULT;
