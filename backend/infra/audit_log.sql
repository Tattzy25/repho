-- Schema for auditing job lifecycle events
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL,
    agent TEXT NOT NULL,
    phase TEXT,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common lookup fields
CREATE INDEX IF NOT EXISTS idx_audit_log_job_id ON audit_log(job_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_agent ON audit_log(agent);
