"""
Initial database schema migration
Uses Alembic for database migrations
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial schema"""
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('username', sa.String(255), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('full_name', sa.String(255)),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Roles table
    op.create_table(
        'roles',
        sa.Column('role_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('role_name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # User roles junction table
    op.create_table(
        'user_roles',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id', ondelete='CASCADE')),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('roles.role_id', ondelete='CASCADE')),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    # Properties table
    op.create_table(
        'properties',
        sa.Column('property_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('street', sa.String(255), nullable=False),
        sa.Column('city', sa.String(255), nullable=False),
        sa.Column('state', sa.String(2), nullable=False),
        sa.Column('zip_code', sa.String(10), nullable=False),
        sa.Column('county', sa.String(255)),
        sa.Column('parcel_number', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('street', 'city', 'state', 'zip_code', 'parcel_number', name='uq_property_address')
    )
    
    # Title searches table
    op.create_table(
        'title_searches',
        sa.Column('search_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('properties.property_id')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('search_type', sa.String(50), nullable=False),
        sa.Column('include_historical', sa.Boolean(), default=False),
        sa.Column('jurisdiction', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('risk_score', sa.Numeric(5, 2)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('completed_at', sa.DateTime(timezone=True))
    )
    op.create_index('idx_title_searches_user_id', 'title_searches', ['user_id'])
    op.create_index('idx_title_searches_property_id', 'title_searches', ['property_id'])
    op.create_index('idx_title_searches_status', 'title_searches', ['status'])
    
    # Deeds table
    op.create_table(
        'deeds',
        sa.Column('deed_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('search_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('title_searches.search_id', ondelete='CASCADE')),
        sa.Column('deed_type', sa.String(100), nullable=False),
        sa.Column('grantor', sa.String(255), nullable=False),
        sa.Column('grantee', sa.String(255), nullable=False),
        sa.Column('recording_date', sa.Date(), nullable=False),
        sa.Column('document_number', sa.String(100), nullable=False),
        sa.Column('book_page', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_deeds_search_id', 'deeds', ['search_id'])
    
    # Liens table
    op.create_table(
        'liens',
        sa.Column('lien_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('search_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('title_searches.search_id', ondelete='CASCADE')),
        sa.Column('lien_type', sa.String(100), nullable=False),
        sa.Column('creditor', sa.String(255), nullable=False),
        sa.Column('amount', sa.Numeric(15, 2)),
        sa.Column('recording_date', sa.Date(), nullable=False),
        sa.Column('document_number', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_liens_search_id', 'liens', ['search_id'])
    
    # Encumbrances table
    op.create_table(
        'encumbrances',
        sa.Column('encumbrance_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('search_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('title_searches.search_id', ondelete='CASCADE')),
        sa.Column('encumbrance_type', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('recording_date', sa.Date(), nullable=False),
        sa.Column('document_number', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_encumbrances_search_id', 'encumbrances', ['search_id'])
    
    # Documents table
    op.create_table(
        'documents',
        sa.Column('document_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('s3_key', sa.String(500)),
        sa.Column('extracted_data', postgresql.JSONB),
        sa.Column('confidence_score', sa.Numeric(5, 2)),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('processed_at', sa.DateTime(timezone=True))
    )
    op.create_index('idx_documents_user_id', 'documents', ['user_id'])
    op.create_index('idx_documents_type', 'documents', ['document_type'])
    op.create_index('idx_documents_status', 'documents', ['status'])
    
    # Risk scores table
    op.create_table(
        'risk_scores',
        sa.Column('score_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('search_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('title_searches.search_id', ondelete='SET NULL')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('property_address', postgresql.JSONB),
        sa.Column('overall_risk_score', sa.Numeric(5, 2), nullable=False),
        sa.Column('risk_level', sa.String(20), nullable=False),
        sa.Column('risk_factors', postgresql.JSONB, nullable=False),
        sa.Column('recommendations', postgresql.ARRAY(sa.Text())),
        sa.Column('model_version', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_risk_scores_search_id', 'risk_scores', ['search_id'])
    op.create_index('idx_risk_scores_user_id', 'risk_scores', ['user_id'])
    
    # Compliance reports table
    op.create_table(
        'compliance_reports',
        sa.Column('report_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('search_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('title_searches.search_id', ondelete='SET NULL')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('property_address', postgresql.JSONB),
        sa.Column('jurisdiction', sa.String(100), nullable=False),
        sa.Column('checks', postgresql.JSONB, nullable=False),
        sa.Column('overall_status', sa.String(20), nullable=False),
        sa.Column('checked_by', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_compliance_reports_search_id', 'compliance_reports', ['search_id'])
    op.create_index('idx_compliance_reports_user_id', 'compliance_reports', ['user_id'])
    
    # Audit logs table
    op.create_table(
        'audit_logs',
        sa.Column('log_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100)),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True)),
        sa.Column('details', postgresql.JSONB),
        sa.Column('ip_address', postgresql.INET),
        sa.Column('user_agent', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'])
    
    # Webhooks table
    op.create_table(
        'webhooks',
        sa.Column('webhook_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('event_types', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('secret', sa.String(255)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_webhooks_user_id', 'webhooks', ['user_id'])
    
    # Webhook deliveries table
    op.create_table(
        'webhook_deliveries',
        sa.Column('delivery_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('webhook_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('webhooks.webhook_id', ondelete='CASCADE')),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('payload', postgresql.JSONB, nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('response_code', sa.Integer()),
        sa.Column('response_body', sa.Text()),
        sa.Column('attempts', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('delivered_at', sa.DateTime(timezone=True))
    )
    op.create_index('idx_webhook_deliveries_webhook_id', 'webhook_deliveries', ['webhook_id'])
    op.create_index('idx_webhook_deliveries_status', 'webhook_deliveries', ['status'])
    
    # Integration configurations table
    op.create_table(
        'integration_configs',
        sa.Column('config_id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id')),
        sa.Column('integration_type', sa.String(100), nullable=False),
        sa.Column('config_data', postgresql.JSONB, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('idx_integration_configs_user_id', 'integration_configs', ['user_id'])
    op.create_index('idx_integration_configs_type', 'integration_configs', ['integration_type'])


def downgrade():
    """Drop all tables"""
    op.drop_table('integration_configs')
    op.drop_table('webhook_deliveries')
    op.drop_table('webhooks')
    op.drop_table('audit_logs')
    op.drop_table('compliance_reports')
    op.drop_table('risk_scores')
    op.drop_table('documents')
    op.drop_table('encumbrances')
    op.drop_table('liens')
    op.drop_table('deeds')
    op.drop_table('title_searches')
    op.drop_table('properties')
    op.drop_table('user_roles')
    op.drop_table('roles')
    op.drop_table('users')

