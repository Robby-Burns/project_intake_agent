from app.pdf.generator import PDFGenerator

def test_pdf_generation():
    """
    Generates a sample PDF to verify formatting.
    """
    print("🚀 Generating Sample PDF...")
    
    generator = PDFGenerator("Sample_Report.pdf")
    
    # Mock Data
    project_name = "Marketing Cloud Storage Migration"
    user_name = "John Doe"
    vp_number = "VP-123"
    
    executive_summary = """
    The user proposes implementing a new cloud storage solution (Dropbox) for the Marketing team. 
    Key drivers are speed of access and storage of large media files. 
    However, significant security and compliance risks were identified regarding PII storage and vendor vetting.
    """
    
    key_findings = [
        "Dropbox is not currently an approved vendor.",
        "PII (Member Photos) will be stored, requiring encryption.",
        "Integration with Active Directory is required for access control."
    ]
    
    specialist_data = {
        "InfoSec": {
            "summary": "The proposal introduces significant data leakage risks. Cloud storage of member data requires strict encryption standards and DLP controls.",
            "questions": [
                {
                    "question": "Is the data encrypted at rest and in transit?",
                    "analysis": "Cloud storage of member data requires strict encryption standards.",
                    "priority": 9
                }
            ]
        },
        "ERM": {
            "summary": "Vendor risk assessment is required. Dropbox is a high-risk vendor due to data hosting location.",
            "questions": [
                {
                    "question": "Has a vendor risk assessment been conducted for Dropbox?",
                    "analysis": "Third-party vendors must undergo due diligence.",
                    "priority": 8
                }
            ]
        },
        "IT Specialist": {
            "summary": "Integration with existing infrastructure is feasible but requires SSO configuration.",
            "questions": [
                {
                    "question": "Does this integrate with our existing Active Directory?",
                    "analysis": "Identity management integration is critical for access control.",
                    "priority": 7
                }
            ]
        }
    }
    
    unanswered_questions = [] # Not used directly anymore, handled via specialist_data
    
    transcript = [
        {"user": "I want to use Dropbox.", "bot": "Okay, tell me more."},
        {"user": "It's for marketing photos.", "bot": "Great. Any security concerns?"},
        {"user": "No, we just need it fast.", "bot": "I see. Let's talk about encryption."}
    ]
    
    success = generator.generate(
        project_name, 
        user_name, 
        vp_number, 
        executive_summary, 
        key_findings,
        specialist_data,
        transcript
    )
    
    if success:
        print("✅ PDF Generated Successfully: Sample_Report.pdf")
    else:
        print("❌ PDF Generation Failed")

if __name__ == "__main__":
    test_pdf_generation()
