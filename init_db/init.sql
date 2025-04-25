-- Create type if it doesn't exist
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statustypes') THEN
        CREATE TYPE statustypes AS ENUM ('PENDING', 'IN_PROGRESS', 'DONE');
    END IF;
END $$;

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS "Tasks" (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status statustypes NOT NULL DEFAULT 'PENDING',
    due_date TIMESTAMPTZ NOT NULL
);