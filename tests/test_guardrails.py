import pytest
from app.guardrails.pii_filter import PIIFilter

class TestPIIFilter:
    
    def test_redact_ssn(self):
        input_text = "My SSN is 123-45-6789."
        expected = "My SSN is [REDACTED_SSN]."
        assert PIIFilter.redact(input_text) == expected

    def test_redact_credit_card(self):
        input_text = "Card: 1234-5678-1234-5678"
        expected = "Card: [REDACTED_CREDIT_CARD]"
        assert PIIFilter.redact(input_text) == expected

    def test_redact_member_id(self):
        input_text = "Member ID 1234567890"
        expected = "Member ID [REDACTED_MEMBER_ID]"
        assert PIIFilter.redact(input_text) == expected

    def test_redact_email(self):
        input_text = "Contact me at test@example.com"
        expected = "Contact me at [REDACTED_EMAIL]"
        assert PIIFilter.redact(input_text) == expected

    def test_validate_vp_number_valid(self):
        assert PIIFilter.validate_vp_number("VP-123") is True

    def test_validate_vp_number_invalid(self):
        assert PIIFilter.validate_vp_number("VP-12") is False
        assert PIIFilter.validate_vp_number("123") is False
        assert PIIFilter.validate_vp_number("VP-ABCD") is False
