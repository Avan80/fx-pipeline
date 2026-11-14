CREATE TABLE IF NOT EXISTS rates (
    id SERIAL PRIMARY KEY,
    base CHAR(3) NOT NULL,
    target CHAR(3) NOT NULL,
    rate NUMERIC(12,4) NOT NULL,
    provider_updated_at TIMESTAMPTZ NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (base, target, provider_updated_at)
);
