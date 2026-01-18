from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Note, db
from datetime import datetime
import bleach

notes_bp = Blueprint('notes', __name__)

# Allowed HTML tags for rich text content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'a', 'code', 'pre', 'span', 'div'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'span': ['style'],
    'div': ['style']
}

@notes_bp.route('/')
@login_required
def index():
    """Display all notes for the current user"""
    return render_template('notes/index.html')

@notes_bp.route('/api/notes')
@login_required
def get_notes():
    """Get all notes for the current user (API endpoint)"""
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        tag = request.args.get('tag', '').strip()
        sort_by = request.args.get('sort', 'updated_at')
        order = request.args.get('order', 'desc')
        archived = request.args.get('archived', 'false') == 'true'
        
        # Base query
        query = Note.query.filter_by(user_id=current_user.id, is_deleted=False, is_archived=archived)
        
        # Apply search filter
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                db.or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term),
                    Note.tags.ilike(search_term)
                )
            )
        
        # Apply tag filter
        if tag:
            query = query.filter(Note.tags.ilike(f'%{tag}%'))
        
        # Apply sorting
        if sort_by == 'title':
            query = query.order_by(Note.title.asc() if order == 'asc' else Note.title.desc())
        elif sort_by == 'created_at':
            query = query.order_by(Note.created_at.asc() if order == 'asc' else Note.created_at.desc())
        else:  # default to updated_at
            query = query.order_by(Note.updated_at.asc() if order == 'asc' else Note.updated_at.desc())
        
        notes = query.all()
        
        return jsonify({
            'success': True,
            'notes': [note.to_dict(include_content=False) for note in notes]
        })
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch notes'}), 500

@notes_bp.route('/api/notes/<int:note_id>')
@login_required
def get_note(note_id):
    """Get a specific note (API endpoint)"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        return jsonify({
            'success': True,
            'note': note.to_dict()
        })
    except Exception as e:
        print(f"Error fetching note: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch note'}), 500

@notes_bp.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    """Create a new note (API endpoint)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        tags = data.get('tags', '')
        
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        if not content:
            return jsonify({'success': False, 'error': 'Content is required'}), 400
        
        # Sanitize content
        clean_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
        
        note = Note(
            user_id=current_user.id,
            title=title,
            content=clean_content,
            tags=tags
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note created successfully',
            'note': note.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating note: {e}")
        return jsonify({'success': False, 'error': 'Failed to create note'}), 500

@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    """Update an existing note (API endpoint)"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        tags = data.get('tags', '')
        
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        if not content:
            return jsonify({'success': False, 'error': 'Content is required'}), 400
        
        # Sanitize content
        clean_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
        
        note.title = title
        note.content = clean_content
        note.tags = tags
        note.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note updated successfully',
            'note': note.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error updating note: {e}")
        return jsonify({'success': False, 'error': 'Failed to update note'}), 500

@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete a note (soft delete) (API endpoint)"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        # Soft delete
        note.is_deleted = True
        note.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting note: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete note'}), 500

@notes_bp.route('/api/notes/<int:note_id>/archive', methods=['POST'])
@login_required
def archive_note(note_id):
    """Archive or unarchive a note (API endpoint)"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        data = request.get_json() or {}
        note.is_archived = data.get('archived', not note.is_archived)
        note.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        action = 'archived' if note.is_archived else 'unarchived'
        return jsonify({
            'success': True,
            'message': f'Note {action} successfully',
            'note': note.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error archiving note: {e}")
        return jsonify({'success': False, 'error': 'Failed to archive note'}), 500

@notes_bp.route('/api/tags')
@login_required
def get_tags():
    """Get all unique tags for the current user"""
    try:
        notes = Note.query.filter_by(user_id=current_user.id, is_deleted=False).all()
        
        tags_set = set()
        for note in notes:
            note_tags = note.get_tags()
            tags_set.update(note_tags)
        
        return jsonify({
            'success': True,
            'tags': sorted(list(tags_set))
        })
    except Exception as e:
        print(f"Error fetching tags: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch tags'}), 500

@notes_bp.route('/new')
@login_required
def new_note():
    """Display new note page"""
    return render_template('notes/edit.html', note=None)

@notes_bp.route('/<int:note_id>')
@login_required
def view_note(note_id):
    """Display a specific note"""
    note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
    
    if not note:
        flash('Note not found', 'error')
        return redirect(url_for('notes.index'))
    
    return render_template('notes/view.html', note=note)

@notes_bp.route('/<int:note_id>/edit')
@login_required
def edit_note(note_id):
    """Display edit note page"""
    note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
    
    if not note:
        flash('Note not found', 'error')
        return redirect(url_for('notes.index'))
    
    return render_template('notes/edit.html', note=note)
