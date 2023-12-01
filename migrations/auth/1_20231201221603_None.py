from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL  DEFAULT False,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(255)  UNIQUE,
    "password" VARCHAR(255) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
CREATE TABLE IF NOT EXISTS "tasks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL  DEFAULT False,
    "task_id" UUID NOT NULL UNIQUE,
    "state" VARCHAR(7) NOT NULL  DEFAULT 'PENDING'
);
COMMENT ON COLUMN "tasks"."state" IS 'SUCCESS: SUCCESS\nPENDING: PENDING\nFAILURE: FALIURE';
CREATE TABLE IF NOT EXISTS "scrap_data" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL  DEFAULT False,
    "topic" VARCHAR(120) NOT NULL,
    "max_people" INT NOT NULL  DEFAULT 20,
    "task_id" BIGINT NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "people" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "is_deleted" BOOL NOT NULL  DEFAULT False,
    "name" VARCHAR(120) NOT NULL,
    "job_description" TEXT NOT NULL,
    "location" VARCHAR(120),
    "additional_data" JSONB,
    "task_id" BIGINT NOT NULL REFERENCES "tasks" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
