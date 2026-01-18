from flask import Blueprint, request, jsonify, send_file, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Note, SharedNote, User, db
from app.services.pdf_service import generate_note_pdf
from app.services.email_service import send_note_email, send_share_notification
from datetime import datetime, timedelta
import io

sharing_bp = Blueprint('sharing', __name__, url_prefix='/share')

@sharing_bp.route('/api/notes/<int:note_id>/share', methods=['POST'])
@login_required
def share_note(note_id):
    """Share a note with another user or create public link"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        data = request.get_json()
        share_type = data.get('type', 'user')  # 'user' or 'link'
        permission = data.get('permission', 'view')  # 'view' or 'edit'
        
        if share_type == 'user':
            # Share with specific user
            username_or_email = data.get('recipient', '').strip()
            
            if not username_or_email:
                return jsonify({'success': False, 'error': 'Recipient is required'}), 400
            
            # Find recipient
            recipient = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email
                )
            ).first()
            
            if not recipient:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            if recipient.id == current_user.id:
                return jsonify({'success': False, 'error': 'Cannot share with yourself'}), 400
            
            # Check if already shared
            existing_share = SharedNote.query.filter_by(
                note_id=note_id,
                owner_id=current_user.id,
                shared_with_user_id=recipient.id
            ).first()
            
            if existing_share:
                # Update existing share
                existing_share.permission_level = permission
                db.session.commit()
                message = 'Share updated successfully'
            else:
                # Create new share
                shared_note = SharedNote(
                    note_id=note_id,
                    owner_id=current_user.id,
                    shared_with_user_id=recipient.id,
                    permission_level=permission
                )
                db.session.add(shared_note)
                db.session.commit()
                message = 'Note shared successfully'
                
                # Send notification email
                share_url = url_for('sharing.view_shared_note', note_id=note_id, _external=True)
                send_share_notification(
                    recipient.email,
                    note.title,
                    share_url,
                    current_user.username,
                    permission
                )
            
            return jsonify({
                'success': True,
                'message': message
            })
        
        elif share_type == 'link':
            # Create shareable link
            expires_days = data.get('expires_days')
            expires_at = None
            
            if expires_days:
                expires_at = datetime.utcnow() + timedelta(days=int(expires_days))
            
            # Check for existing public link
            existing_link = SharedNote.query.filter_by(
                note_id=note_id,
                owner_id=current_user.id,
                shared_with_user_id=None
            ).filter(SharedNote.share_token.isnot(None)).first()
            
            if existing_link:
                # Update existing link
                existing_link.permission_level = permission
                existing_link.expires_at = expires_at
                share_token = existing_link.share_token
                db.session.commit()
            else:
                # Create new link
                share_token = SharedNote.generate_token()
                shared_note = SharedNote(
                    note_id=note_id,
                    owner_id=current_user.id,
                    share_token=share_token,
                    permission_level=permission,
                    expires_at=expires_at
                )
                db.session.add(shared_note)
                db.session.commit()
            
            share_url = url_for('sharing.view_public_note', token=share_token, _external=True)
            
            return jsonify({
                'success': True,
                'message': 'Share link created successfully',
                'share_url': share_url,
                'expires_at': expires_at.isoformat() if expires_at else None
            })
        
        else:
            return jsonify({'success': False, 'error': 'Invalid share type'}), 400
    
    except Exception as e:
        db.session.rollback()
        print(f"Error sharing note: {e}")
        return jsonify({'success': False, 'error': 'Failed to share note'}), 500

@sharing_bp.route('/api/notes/<int:note_id>/shares')
@login_required
def get_shares(note_id):
    """Get all shares for a note"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        shares = SharedNote.query.filter_by(note_id=note_id, owner_id=current_user.id).all()
        
        shares_data = []
        for share in shares:
            share_dict = share.to_dict()
            if share.shared_with_user_id:
                recipient = User.query.get(share.shared_with_user_id)
                share_dict['recipient_username'] = recipient.username if recipient else None
                share_dict['recipient_email'] = recipient.email if recipient else None
            if share.share_token:
                share_dict['share_url'] = url_for('sharing.view_public_note', token=share.share_token, _external=True)
            shares_data.append(share_dict)
        
        return jsonify({
            'success': True,
            'shares': shares_data
        })
    except Exception as e:
        print(f"Error fetching shares: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch shares'}), 500

@sharing_bp.route('/api/shares/<int:share_id>', methods=['DELETE'])
@login_required
def revoke_share(share_id):
    """Revoke a share"""
    try:
        share = SharedNote.query.filter_by(id=share_id, owner_id=current_user.id).first()
        
        if not share:
            return jsonify({'success': False, 'error': 'Share not found'}), 404
        
        db.session.delete(share)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Share revoked successfully'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error revoking share: {e}")
        return jsonify({'success': False, 'error': 'Failed to revoke share'}), 500

@sharing_bp.route('/<int:note_id>')
@login_required
def view_shared_note(note_id):
    """View a note shared with the current user"""
    # Check if user has access to this note
    share = SharedNote.query.filter_by(
        note_id=note_id,
        shared_with_user_id=current_user.id
    ).first()
    
    if not share:
        # Check if user owns the note
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        if not note:
            flash('You do not have access to this note', 'error')
            return redirect(url_for('notes.index'))
    else:
        note = Note.query.filter_by(id=note_id, is_deleted=False).first()
        if not note:
            flash('Note not found', 'error')
            return redirect(url_for('notes.index'))
    
    return render_template('shared/view.html', note=note, share=share)

@sharing_bp.route('/public/<token>')
def view_public_note(token):
    """View a publicly shared note via token"""
    share = SharedNote.query.filter_by(share_token=token).first()
    
    if not share:
        flash('Invalid share link', 'error')
        return redirect(url_for('auth.login'))
    
    if share.is_expired():
        flash('This share link has expired', 'error')
        return redirect(url_for('auth.login'))
    
    note = Note.query.filter_by(id=share.note_id, is_deleted=False).first()
    
    if not note:
        flash('Note not found', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('shared/public.html', note=note, share=share)

@sharing_bp.route('/api/notes/<int:note_id>/export/pdf')
@login_required
def export_pdf(note_id):
    """Export note as PDF"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        # Generate PDF
        pdf_buffer = generate_note_pdf(note, current_user)
        
        # Send file
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{note.title}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error exporting PDF: {e}")
        return jsonify({'success': False, 'error': 'Failed to export PDF'}), 500

@sharing_bp.route('/api/notes/<int:note_id>/export/text')
@login_required
def export_text(note_id):
    """Export note as text file"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        # Create text content
        text_content = f"{note.title}\n\n"
        text_content += f"Created: {note.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        text_content += f"Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        if note.tags:
            text_content += f"Tags: {note.tags}\n"
        
        text_content += f"\n{'-' * 50}\n\n"
        text_content += note.content
        
        # Create file buffer
        text_buffer = io.BytesIO(text_content.encode('utf-8'))
        text_buffer.seek(0)
        
        # Send file
        return send_file(
            text_buffer,
            as_attachment=True,
            download_name=f"{note.title}.txt",
            mimetype='text/plain'
        )
    except Exception as e:
        print(f"Error exporting text: {e}")
        return jsonify({'success': False, 'error': 'Failed to export text'}), 500

@sharing_bp.route('/api/notes/<int:note_id>/email', methods=['POST'])
@login_required
def email_note(note_id):
    """Send note via email"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id, is_deleted=False).first()
        
        if not note:
            return jsonify({'success': False, 'error': 'Note not found'}), 404
        
        data = request.get_json()
        recipient_email = data.get('email', '').strip()
        
        if not recipient_email:
            return jsonify({'success': False, 'error': 'Recipient email is required'}), 400
        
        # Send email
        success = send_note_email(
            recipient_email,
            note.title,
            note.content,
            current_user.username
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Note sent via email successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send email'
            }), 500
    
    except Exception as e:
        print(f"Error emailing note: {e}")
        return jsonify({'success': False, 'error': 'Failed to send email'}), 500
