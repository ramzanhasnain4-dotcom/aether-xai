-- Schema Isolation & Base Tables for Aether-XAI Engine

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tenant_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    max_risk_threshold NUMERIC(5, 4) NOT NULL DEFAULT 0.7500,
    enforce_symbolic_check BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ml_inference_audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    raw_prediction NUMERIC(5, 4) NOT NULL,
    constraint_passed BOOLEAN NOT NULL,
    explanation_json JSONB NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);