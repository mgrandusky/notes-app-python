from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
import html

def generate_pdf(note_title, note_content, author_name, created_at, tags=None):
    """
    Generate a PDF from note content
    
    Args:
        note_title: Title of the note
        note_content: Content of the note (can include HTML)
        author_name: Name of the note author
        created_at: Creation timestamp
        tags: Optional list of tags
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    # Custom metadata style
    meta_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#7f8c8d',
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    # Custom content style
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=12,
        leading=16,
        spaceAfter=12,
        alignment=TA_LEFT,
    )
    
    # Add title
    title = Paragraph(html.escape(note_title), title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Add metadata
    meta_info = f"Author: {html.escape(author_name)}"
    if created_at:
        if isinstance(created_at, str):
            meta_info += f" | Created: {created_at}"
        else:
            meta_info += f" | Created: {created_at.strftime('%Y-%m-%d %H:%M')}"
    
    if tags:
        tags_str = ', '.join(tags) if isinstance(tags, list) else tags
        meta_info += f" | Tags: {html.escape(tags_str)}"
    
    metadata = Paragraph(meta_info, meta_style)
    elements.append(metadata)
    elements.append(Spacer(1, 12))
    
    # Add a line separator
    elements.append(Spacer(1, 12))
    
    # Process and add content
    # Handle basic HTML tags and convert to paragraphs
    content_paragraphs = note_content.split('\n')
    
    for para in content_paragraphs:
        if para.strip():
            # Escape HTML to prevent issues, but preserve basic formatting
            safe_para = html.escape(para.strip())
            p = Paragraph(safe_para, content_style)
            elements.append(p)
            elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    
    # Get the PDF data
    buffer.seek(0)
    return buffer

def generate_note_pdf(note, author):
    """
    Generate PDF for a Note model instance
    
    Args:
        note: Note model instance
        author: User model instance
    
    Returns:
        BytesIO object containing the PDF
    """
    return generate_pdf(
        note_title=note.title,
        note_content=note.content,
        author_name=author.username,
        created_at=note.created_at,
        tags=note.get_tags()
    )
