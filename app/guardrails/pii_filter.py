import re
import os
from typing import List, Optional
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PIIFilter:
    """
    Hybrid PII Redaction: Presidio (NLP) + Regex Fallback.
    Ensures high accuracy even with small models by using Regex for strict patterns.
    """
    
    _analyzer = None
    _anonymizer = None
    
    # Regex Patterns (Fallback/Baseline)
    REGEX_PATTERNS = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "MEMBER_ID": r"\b\d{8,10}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    }

    @classmethod
    def _initialize(cls):
        """
        Lazy initialization of Presidio engines.
        """
        if cls._analyzer is None:
            model_name = os.getenv("SPACY_MODEL", "en_core_web_sm")
            
            configuration = {
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": model_name}],
            }
            
            provider = NlpEngineProvider(nlp_configuration=configuration)
            nlp_engine = provider.create_engine()

            cls._analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
            cls._anonymizer = AnonymizerEngine()

    @classmethod
    def redact(cls, text: str, allow_list: Optional[List[str]] = None) -> str:
        """
        Scans text for PII using Hybrid approach (Regex + NLP).

        Args:
            text: Input text.
            allow_list: List of Presidio entity types to IGNORE (e.g., ['PERSON']).
        """
        if not text:
            return ""

        allow_list = allow_list or []

        # 1. Regex Redaction (Baseline - Fast & Strict)
        # We do this FIRST to catch obvious patterns that the small model might miss
        sanitized_text = text
        for pii_type, pattern in cls.REGEX_PATTERNS.items():
            # If EMAIL is allowed, skip regex for it
            if pii_type == "EMAIL" and "EMAIL_ADDRESS" in allow_list:
                continue

            sanitized_text = re.sub(
                pattern, 
                f"[REDACTED_{pii_type}]", 
                sanitized_text
            )
            
        # 2. Presidio Redaction (NLP - Context Aware)
        # Catches things Regex missed (e.g., names, phone numbers in weird formats)
        cls._initialize()

        # Default entities to check
        entities_to_check = ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "US_SSN", "US_BANK_NUMBER"]

        # Remove allowed entities
        entities_to_check = [e for e in entities_to_check if e not in allow_list]

        results = cls._analyzer.analyze(
            text=sanitized_text,
            entities=entities_to_check,
            language='en'
        )
        
        # Define custom operators to match our output format [REDACTED_TYPE]
        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "[REDACTED_PERSON]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[REDACTED_PHONE]"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[REDACTED_EMAIL]"}),
            "US_SSN": OperatorConfig("replace", {"new_value": "[REDACTED_SSN]"}),
            "US_BANK_NUMBER": OperatorConfig("replace", {"new_value": "[REDACTED_BANK_ACCT]"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "[REDACTED_CREDIT_CARD]"}),
        }
        
        anonymized_result = cls._anonymizer.anonymize(
            text=sanitized_text,
            analyzer_results=results,
            operators=operators
        )
        
        return anonymized_result.text

    @classmethod
    def validate_vp_number(cls, vp_number: str) -> bool:
        """
        Validates VP Number format (e.g., VP-123).
        """
        pattern = r"^VP-\d{3}$"
        return bool(re.match(pattern, vp_number))
