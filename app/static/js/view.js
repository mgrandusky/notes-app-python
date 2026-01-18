// Note View Page Scripts
let currentNoteId;

// Share Modal
function shareNote(noteId) {
    currentNoteId = noteId;
    document.getElementById('share-modal').style.display = 'flex';
}

function closeShareModal() {
    document.getElementById('share-modal').style.display = 'none';
}

// Tab Navigation
document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            // Update tab buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelector(`[data-tab-content="${tab}"]`).classList.add('active');
        });
    });
});

// Share with User
async function shareWithUser() {
    const recipient = document.getElementById('share-recipient').value.trim();
    const permission = document.getElementById('share-permission-user').value;
    
    if (!recipient) {
        showToast('Please enter a username or email', 'error');
        return;
    }
    
    try {
        await apiRequest(`/share/api/notes/${currentNoteId}/share`, {
            method: 'POST',
            body: JSON.stringify({
                type: 'user',
                recipient,
                permission
            })
        });
        
        showToast('Note shared successfully', 'success');
        document.getElementById('share-recipient').value = '';
    } catch (error) {
        showToast(error.message || 'Failed to share note', 'error');
    }
}

// Create Share Link
async function createShareLink() {
    const permission = document.getElementById('share-permission-link').value;
    const expires = document.getElementById('share-expires').value;
    
    try {
        const data = await apiRequest(`/share/api/notes/${currentNoteId}/share`, {
            method: 'POST',
            body: JSON.stringify({
                type: 'link',
                permission,
                expires_days: expires || null
            })
        });
        
        if (data.share_url) {
            const resultDiv = document.getElementById('share-link-result');
            const urlInput = document.getElementById('share-link-url');
            urlInput.value = data.share_url;
            resultDiv.style.display = 'flex';
            showToast('Share link created successfully', 'success');
        }
    } catch (error) {
        showToast(error.message || 'Failed to create share link', 'error');
    }
}

// Copy Share Link
function copyShareLink() {
    const urlInput = document.getElementById('share-link-url');
    urlInput.select();
    document.execCommand('copy');
    showToast('Link copied to clipboard', 'success');
}

// Email Note
async function emailNote() {
    const email = document.getElementById('email-recipient').value.trim();
    
    if (!email) {
        showToast('Please enter an email address', 'error');
        return;
    }
    
    try {
        await apiRequest(`/share/api/notes/${currentNoteId}/email`, {
            method: 'POST',
            body: JSON.stringify({ email })
        });
        
        showToast('Note sent via email successfully', 'success');
        document.getElementById('email-recipient').value = '';
    } catch (error) {
        showToast(error.message || 'Failed to send email', 'error');
    }
}

// Export Functions
function exportNote(noteId) {
    currentNoteId = noteId;
    shareNote(noteId);
    // Switch to export tab
    document.querySelector('[data-tab="export"]').click();
}

function exportToPDF() {
    window.location.href = `/share/api/notes/${currentNoteId}/export/pdf`;
    showToast('Downloading PDF...', 'info');
}

function exportToText() {
    window.location.href = `/share/api/notes/${currentNoteId}/export/text`;
    showToast('Downloading text file...', 'info');
}

// Delete Note
function deleteNote(noteId) {
    currentNoteId = noteId;
    openDeleteModal(noteId);
}

function openDeleteModal(noteId) {
    document.getElementById('delete-modal').style.display = 'flex';
}

function closeDeleteModal() {
    document.getElementById('delete-modal').style.display = 'none';
}

async function confirmDelete() {
    try {
        await apiRequest(`/api/notes/${currentNoteId}`, {
            method: 'DELETE'
        });
        
        showToast('Note deleted successfully', 'success');
        setTimeout(() => {
            window.location.href = '/notes';
        }, 1000);
    } catch (error) {
        showToast('Failed to delete note', 'error');
    }
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});
