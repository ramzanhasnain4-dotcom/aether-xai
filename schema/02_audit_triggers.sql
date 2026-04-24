-- Automated PL/pgSQL Audit Trigger

CREATE OR REPLACE FUNCTION log_inference_event()
RETURNS TRIGGER AS $$
BEGIN
    -- Automatically attach current active tenant from session settings if unassigned
    IF NEW.tenant_id IS NULL THEN
        NEW.tenant_id := NULLIF(current_setting('app.current_tenant_id', true), '')::uuid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_inference_event
    BEFORE INSERT ON ml_inference_audits
    FOR EACH ROW
    EXECUTE FUNCTION log_inference_event();