from app.models.user import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Text

class Note(db.Model):
    """Note model for storing user notes"""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    is_archived = db.Column(db.Boolean, default=False, index=True)
    
    # Relationships
    shares = db.relationship('SharedNote', backref='note', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Note {self.title}>'
    
    def to_dict(self, include_content=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'tags': self.get_tags(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_archived': self.is_archived
        }
        if include_content:
            data['content'] = self.content
        return data
    
    def get_tags(self):
        """Parse tags from string to list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags(self, tag_list):
        """Set tags from list to string"""
        if isinstance(tag_list, list):
            self.tags = ', '.join(tag_list)
        else:
            self.tags = tag_list
