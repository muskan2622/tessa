-- Real Estate TC Agent Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User roles junction table
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(role_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Properties table
CREATE TABLE properties (
    property_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    street VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    county VARCHAR(255),
    parcel_number VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(street, city, state, zip_code, parcel_number)
);

-- Title searches table
CREATE TABLE title_searches (
    search_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    property_id UUID REFERENCES properties(property_id),
    user_id UUID REFERENCES users(user_id),
    search_type VARCHAR(50) NOT NULL,
    include_historical BOOLEAN DEFAULT FALSE,
    jurisdiction VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    risk_score DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    INDEX idx_title_searches_user_id (user_id),
    INDEX idx_title_searches_property_id (property_id),
    INDEX idx_title_searches_status (status)
);

-- Deeds table
CREATE TABLE deeds (
    deed_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    search_id UUID REFERENCES title_searches(search_id) ON DELETE CASCADE,
    deed_type VARCHAR(100) NOT NULL,
    grantor VARCHAR(255) NOT NULL,
    grantee VARCHAR(255) NOT NULL,
    recording_date DATE NOT NULL,
    document_number VARCHAR(100) NOT NULL,
    book_page VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_deeds_search_id (search_id)
);

-- Liens table
CREATE TABLE liens (
    lien_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    search_id UUID REFERENCES title_searches(search_id) ON DELETE CASCADE,
    lien_type VARCHAR(100) NOT NULL,
    creditor VARCHAR(255) NOT NULL,
    amount DECIMAL(15,2),
    recording_date DATE NOT NULL,
    document_number VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_liens_search_id (search_id)
);

-- Encumbrances table
CREATE TABLE encumbrances (
    encumbrance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    search_id UUID REFERENCES title_searches(search_id) ON DELETE CASCADE,
    encumbrance_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    recording_date DATE NOT NULL,
    document_number VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_encumbrances_search_id (search_id)
);

-- Documents table
CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    s3_key VARCHAR(500),
    extracted_data JSONB,
    confidence_score DECIMAL(5,2),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    INDEX idx_documents_user_id (user_id),
    INDEX idx_documents_type (document_type),
    INDEX idx_documents_status (status)
);

-- Risk scores table
CREATE TABLE risk_scores (
    score_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    search_id UUID REFERENCES title_searches(search_id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(user_id),
    property_address JSONB,
    overall_risk_score DECIMAL(5,2) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_factors JSONB NOT NULL,
    recommendations TEXT[],
    model_version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_risk_scores_search_id (search_id),
    INDEX idx_risk_scores_user_id (user_id)
);

-- Compliance reports table
CREATE TABLE compliance_reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    search_id UUID REFERENCES title_searches(search_id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(user_id),
    property_address JSONB,
    jurisdiction VARCHAR(100) NOT NULL,
    checks JSONB NOT NULL,
    overall_status VARCHAR(20) NOT NULL,
    checked_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_compliance_reports_search_id (search_id),
    INDEX idx_compliance_reports_user_id (user_id)
);

-- Audit logs table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_logs_user_id (user_id),
    INDEX idx_audit_logs_created_at (created_at)
);

-- Webhooks table
CREATE TABLE webhooks (
    webhook_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    url VARCHAR(500) NOT NULL,
    event_types TEXT[] NOT NULL,
    secret VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_webhooks_user_id (user_id)
);

-- Webhook deliveries table
CREATE TABLE webhook_deliveries (
    delivery_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    webhook_id UUID REFERENCES webhooks(webhook_id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) NOT NULL,
    response_code INTEGER,
    response_body TEXT,
    attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP WITH TIME ZONE,
    INDEX idx_webhook_deliveries_webhook_id (webhook_id),
    INDEX idx_webhook_deliveries_status (status)
);

-- Integration configurations table
CREATE TABLE integration_configs (
    config_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    integration_type VARCHAR(100) NOT NULL, -- 'salesforce', 'hubspot', 'qualia', etc.
    config_data JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_integration_configs_user_id (user_id),
    INDEX idx_integration_configs_type (integration_type)
);

