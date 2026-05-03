-- =====================================================
-- DATABASE SCHEMA - Hệ thống Nhắc hạn Văn bản
-- Dành cho Supabase PostgreSQL (DB hoàn toàn mới)
-- =====================================================

BEGIN;

-- 1. Phòng ban
CREATE TABLE departments (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    parent_id UUID,
    manager_id UUID,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(parent_id) REFERENCES departments (id),
    UNIQUE (code)
);

-- 2. Người dùng
CREATE TABLE users (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    department_id UUID,
    position VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    can_login BOOLEAN NOT NULL DEFAULT false,
    manager_id UUID,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(department_id) REFERENCES departments (id),
    FOREIGN KEY(manager_id) REFERENCES users (id),
    UNIQUE (email)
);

-- FK vòng: departments.manager_id -> users.id
ALTER TABLE departments ADD CONSTRAINT fk_departments_manager_id_users 
    FOREIGN KEY(manager_id) REFERENCES users (id);

-- 3. Văn bản
CREATE TABLE documents (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    document_number VARCHAR(100),
    description TEXT,
    owner_id UUID NOT NULL,
    department_id UUID NOT NULL,
    expiry_date DATE NOT NULL,
    file_path VARCHAR(1000),
    file_name VARCHAR(255),
    file_size INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(department_id) REFERENCES departments (id),
    FOREIGN KEY(owner_id) REFERENCES users (id)
);

-- 4. Quy tắc nhắc nhở
CREATE TABLE reminder_rules (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    days_before INTEGER NOT NULL,
    is_overdue_rule BOOLEAN NOT NULL DEFAULT false,
    channel VARCHAR(20) NOT NULL DEFAULT 'email',
    is_active BOOLEAN NOT NULL DEFAULT true,
    subject_template VARCHAR(255),
    body_template TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);

-- 5. Lịch sử gửi email
CREATE TABLE reminder_logs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    rule_id UUID NOT NULL,
    recipient_user_id UUID NOT NULL,
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    message TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    provider_response TEXT,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(document_id) REFERENCES documents (id),
    FOREIGN KEY(recipient_user_id) REFERENCES users (id),
    FOREIGN KEY(rule_id) REFERENCES reminder_rules (id),
    CONSTRAINT uq_reminder_log_doc_rule_user UNIQUE (document_id, rule_id, recipient_user_id)
);

-- 6. Cài đặt hệ thống (Key-Value)
CREATE TABLE system_settings (
    key VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    description VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (key)
);

COMMIT;
