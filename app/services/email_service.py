from flask_mail import Mail, Message
from flask import render_template, current_app
from threading import Thread

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail"""
    mail.init_app(app)
    return mail

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

def send_email(subject, recipient, text_body, html_body=None):
    """Send email with optional HTML body"""
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient] if isinstance(recipient, str) else recipient,
            body=text_body,
            html=html_body
        )
        
        # Send asynchronously
        app = current_app._get_current_object()
        Thread(target=send_async_email, args=(app, msg)).start()
        return True
    except Exception as e:
        print(f"Error creating email: {e}")
        return False

def send_note_email(recipient_email, note_title, note_content, sender_name):
    """Send a note via email"""
    subject = f"Shared Note: {note_title}"
    text_body = f"""
{sender_name} has shared a note with you.

Title: {note_title}

Content:
{note_content}

---
Sent from Notes App
"""
    
    html_body = f"""
<html>
<body>
    <h2>Shared Note from {sender_name}</h2>
    <h3>{note_title}</h3>
    <div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #007bff;">
        {note_content}
    </div>
    <p style="margin-top: 20px; color: #666; font-size: 12px;">
        Sent from Notes App
    </p>
</body>
</html>
"""
    
    return send_email(subject, recipient_email, text_body, html_body)

def send_share_notification(recipient_email, note_title, share_url, sender_name, permission):
    """Send notification when a note is shared"""
    subject = f"{sender_name} shared a note with you"
    text_body = f"""
{sender_name} has shared a note titled "{note_title}" with you.

Permission: {permission}

Access the note here: {share_url}

---
Sent from Notes App
"""
    
    html_body = f"""
<html>
<body>
    <h2>Note Shared With You</h2>
    <p><strong>{sender_name}</strong> has shared a note with you.</p>
    <h3>{note_title}</h3>
    <p><strong>Permission:</strong> {permission}</p>
    <p style="margin-top: 20px;">
        <a href="{share_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
            View Note
        </a>
    </p>
    <p style="margin-top: 20px; color: #666; font-size: 12px;">
        Sent from Notes App
    </p>
</body>
</html>
"""
    
    return send_email(subject, recipient_email, text_body, html_body)
