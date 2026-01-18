from app.models.user import db
from datetime import datetime
import secrets

class SharedNote(db.Model):
    """Shared note model for managing note sharing"""
    __tablename__ = 'shared_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    share_token = db.Column(db.String(64), unique=True, nullable=True, index=True)
    permission_level = db.Column(db.String(10), default='view')
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SharedNote {self.note_id}>'
    
    @staticmethod
    def generate_token():
        """Generate a unique share token"""
        return secrets.token_urlsafe(32)
    
    def is_expired(self):
        """Check if share link has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'note_id': self.note_id,
            'owner_id': self.owner_id,
            'shared_with_user_id': self.shared_with_user_id,
            'share_token': self.share_token,
            'permission_level': self.permission_level,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_expired': self.is_expired()
        }
