from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from typing import List, Dict
import datetime
import os

class PDFGenerator:
    """
    Generates the Project Intake Report.
    Includes: Executive Summary, Key Findings, Specialist Analysis, and Full Transcript.
    """
    
    def __init__(self, filename: str = "Project_Intake_Report.pdf"):
        # Ensure reports directory exists
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.filename = os.path.join(self.output_dir, filename)
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Define custom styles for the report."""
        self.styles.add(ParagraphStyle(
            name='SpecialistHeader',
            parent=self.styles['Heading2'],
            textColor=colors.darkblue,
            spaceBefore=12,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='DomainSummary',
            parent=self.styles['BodyText'],
            textColor=colors.black,
            backColor=colors.aliceblue,
            borderPadding=8,
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='TranscriptUser',
            parent=self.styles['BodyText'],
            textColor=colors.black,
            backColor=colors.whitesmoke,
            borderPadding=5
        ))
        self.styles.add(ParagraphStyle(
            name='TranscriptBot',
            parent=self.styles['BodyText'],
            textColor=colors.darkblue,
            borderPadding=5
        ))

    def generate(self, 
                 project_name: str,
                 user_name: str,
                 vp_number: str,
                 stakeholders: str,
                 executive_summary: str,
                 key_findings: List[str],
                 specialist_data: Dict[str, Dict], # {agent_name: {'summary': str, 'questions': list}}
                 transcript: List[Dict]):
        """
        Builds the PDF document.
        """
        # Update filename with directory if it was changed externally
        if not self.filename.startswith(self.output_dir):
             self.filename = os.path.join(self.output_dir, os.path.basename(self.filename))

        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        story = []

        # 1. Title & Metadata
        story.append(Paragraph("Project Intake Analysis Report", self.styles['Title']))
        story.append(Spacer(1, 12))
        
        # Metadata Table
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = [
            ["Project Name:", project_name],
            ["Requester Name:", user_name],
            ["VP Number:", vp_number],
            ["Stakeholders:", stakeholders],
            ["Generated On:", timestamp]
        ]
        t = Table(meta_data, colWidths=[120, 300], hAlign='LEFT')
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,0), (0,-1), colors.darkblue),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 24))

        # 2. Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['Heading1']))
        story.append(Paragraph(executive_summary, self.styles['BodyText']))
        story.append(Spacer(1, 12))

        # 3. Key Findings
        if key_findings:
            story.append(Paragraph("Key Findings", self.styles['Heading2']))
            bullet_points = []
            for finding in key_findings:
                bullet_points.append(ListItem(Paragraph(finding, self.styles['BodyText'])))
            story.append(ListFlowable(bullet_points, bulletType='bullet', start='circle'))
            story.append(Spacer(1, 24))

        # 4. Specialist Sections (Summary + Questions)
        story.append(Paragraph("Specialist Analysis", self.styles['Heading1']))
        
        # Define order of specialists
        specialist_order = [
            "Project Manager", "Product Manager", "IT Specialist", 
            "InfoSec", "ERM", "Training", "Marketing", "Accounting"
        ]
        
        for agent_name in specialist_order:
            data = specialist_data.get(agent_name)
            if not data:
                continue
                
            # Group content to keep header with summary
            content = []
            
            # Header
            content.append(Paragraph(agent_name, self.styles['SpecialistHeader']))
            
            # Domain Summary
            summary = data.get('summary', 'No summary provided.')
            content.append(Paragraph(f"<b>{agent_name} Summary:</b><br/>{summary}", self.styles['DomainSummary']))
            
            # Questions
            questions = data.get('questions', [])
            if questions:
                content.append(Paragraph("<b>Critical Questions & Analysis:</b>", self.styles['BodyText']))
                for q in questions:
                    q_text = q.get('question', '')
                    analysis = q.get('analysis', '')
                    priority = q.get('priority', 0)
                    
                    q_block = f"• <b>[Priority {priority}]</b> {q_text}<br/><i>Analysis: {analysis}</i>"
                    content.append(Paragraph(q_block, self.styles['BodyText']))
                    content.append(Spacer(1, 6))
            else:
                content.append(Paragraph("<i>No critical questions identified.</i>", self.styles['BodyText']))
            
            content.append(Spacer(1, 12))
            story.append(KeepTogether(content))

        story.append(Spacer(1, 24))

        # 5. Full Transcript
        story.append(Paragraph("Interview Transcript", self.styles['Heading1']))
        
        for entry in transcript:
            user_text = f"<b>User:</b> {entry.get('user', '')}"
            bot_text = f"<b>Bot:</b> {entry.get('bot', '')}"
            
            story.append(Paragraph(user_text, self.styles['TranscriptUser']))
            story.append(Spacer(1, 6))
            story.append(Paragraph(bot_text, self.styles['TranscriptBot']))
            story.append(Spacer(1, 12))

        # Build
        try:
            doc.build(story)
            return True
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
