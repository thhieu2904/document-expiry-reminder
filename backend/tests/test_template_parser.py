"""
Unit tests for the email template parser (parse_template).
Tests all supported tags, edge cases (empty template, None dept, overdue docs).
"""
import uuid
from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest

# We can't import the ORM models directly without a DB engine,
# so we mock them with simple objects that have the same attributes.


def _make_doc(title="Giấy phép XD 123", doc_number="GP-2025-001", expiry_date=date(2025, 6, 15)):
    doc = MagicMock()
    doc.title = title
    doc.document_number = doc_number
    doc.expiry_date = expiry_date
    return doc


def _make_owner(full_name="Nguyễn Văn A", email="a@hcc.gov.vn", department_id=uuid.uuid4()):
    owner = MagicMock()
    owner.full_name = full_name
    owner.email = email
    owner.department_id = department_id
    return owner


def _make_dept(name="Phòng Hành chính"):
    dept = MagicMock()
    dept.name = name
    return dept


def _make_rule(name="Nhắc trước 7 ngày"):
    rule = MagicMock()
    rule.name = name
    return rule


# Import the function under test
from app.services.reminder_engine import parse_template


class TestParseTemplate:
    """Tests for parse_template()."""

    def setup_method(self):
        self.doc = _make_doc()
        self.owner = _make_owner()
        self.dept = _make_dept()
        self.rule = _make_rule()
        self.today = date(2025, 6, 10)  # 5 days before expiry

    # --- Basic tag replacement ---

    def test_document_title(self):
        result = parse_template("VB: {{document_title}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "VB: Giấy phép XD 123"

    def test_document_number(self):
        result = parse_template("Số: {{document_number}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Số: GP-2025-001"

    def test_department_name(self):
        result = parse_template("PB: {{department_name}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "PB: Phòng Hành chính"

    def test_expiry_date(self):
        result = parse_template("Hạn: {{expiry_date}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Hạn: 15/06/2025"

    def test_rule_name(self):
        result = parse_template("QT: {{rule_name}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "QT: Nhắc trước 7 ngày"

    def test_days_left(self):
        result = parse_template("Còn {{days_left}} ngày", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Còn 5 ngày"

    def test_owner_name(self):
        result = parse_template("Gửi: {{owner_name}}", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Gửi: Nguyễn Văn A"

    # --- Combined tags ---

    def test_multiple_tags_in_one_template(self):
        template = "Kính gửi {{owner_name}} ({{department_name}}), văn bản {{document_number}} - {{document_title}} hết hạn ngày {{expiry_date}}, còn {{days_left}} ngày."
        result = parse_template(template, self.doc, self.owner, self.dept, self.rule, self.today)
        expected = "Kính gửi Nguyễn Văn A (Phòng Hành chính), văn bản GP-2025-001 - Giấy phép XD 123 hết hạn ngày 15/06/2025, còn 5 ngày."
        assert result == expected

    def test_subject_template(self):
        template = "[{{rule_name}}] {{document_number}} - {{document_title}}"
        result = parse_template(template, self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "[Nhắc trước 7 ngày] GP-2025-001 - Giấy phép XD 123"

    # --- Edge cases ---

    def test_empty_template_returns_empty(self):
        result = parse_template("", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == ""

    def test_none_template_returns_empty(self):
        result = parse_template(None, self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == ""

    def test_no_tags_returns_plain_text(self):
        result = parse_template("Đây là văn bản thuần.", self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Đây là văn bản thuần."

    def test_none_department_shows_fallback(self):
        result = parse_template("PB: {{department_name}}", self.doc, self.owner, None, self.rule, self.today)
        assert result == "PB: Không có"

    def test_none_document_number_shows_fallback(self):
        doc = _make_doc(doc_number=None)
        result = parse_template("Số: {{document_number}}", doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Số: Không có"

    def test_overdue_days_left_is_negative(self):
        """When today > expiry_date, days_left should be negative."""
        today_overdue = date(2025, 6, 20)  # 5 days AFTER expiry
        result = parse_template("Quá hạn {{days_left}} ngày", self.doc, self.owner, self.dept, self.rule, today_overdue)
        assert result == "Quá hạn -5 ngày"

    def test_owner_without_full_name_falls_back_to_email(self):
        owner = _make_owner(full_name=None)
        result = parse_template("Gửi: {{owner_name}}", self.doc, owner, self.dept, self.rule, self.today)
        assert result == "Gửi: a@hcc.gov.vn"

    def test_duplicate_tag_replaced_all_occurrences(self):
        template = "{{document_title}} và lại {{document_title}}"
        result = parse_template(template, self.doc, self.owner, self.dept, self.rule, self.today)
        assert result == "Giấy phép XD 123 và lại Giấy phép XD 123"
