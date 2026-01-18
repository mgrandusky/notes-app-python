// Rich Text Editor
let editor;

// Initialize Editor
function initEditor() {
    editor = document.getElementById('note-content');
    
    if (!editor) return;
    
    // Setup toolbar buttons
    const toolbarButtons = document.querySelectorAll('.toolbar-btn');
    toolbarButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const command = btn.dataset.command;
            const value = btn.dataset.value || null;
            executeCommand(command, value);
        });
    });
    
    // Keyboard shortcuts
    editor.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key.toLowerCase()) {
                case 'b':
                    e.preventDefault();
                    executeCommand('bold');
                    break;
                case 'i':
                    e.preventDefault();
                    executeCommand('italic');
                    break;
                case 'u':
                    e.preventDefault();
                    executeCommand('underline');
                    break;
            }
        }
    });
}

// Execute Editor Command
function executeCommand(command, value = null) {
    document.execCommand(command, false, value);
    editor.focus();
}

// Save Note
async function saveNote() {
    const noteId = document.getElementById('note-id').value;
    const title = document.getElementById('note-title').value.trim();
    const content = editor.innerHTML;
    const tags = document.getElementById('note-tags').value.trim();
    
    if (!title) {
        showToast('Please enter a title', 'error');
        return;
    }
    
    if (!content || content === '<br>' || content === '<div><br></div>') {
        showToast('Please enter some content', 'error');
        return;
    }
    
    const saveBtn = document.getElementById('save-btn');
    const saveStatus = document.getElementById('save-status');
    
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';
    saveStatus.textContent = 'Saving...';
    
    try {
        const url = noteId ? `/api/notes/${noteId}` : '/api/notes';
        const method = noteId ? 'PUT' : 'POST';
        
        const data = await apiRequest(url, {
            method,
            body: JSON.stringify({
                title,
                content,
                tags
            })
        });
        
        showToast(data.message || 'Note saved successfully', 'success');
        saveStatus.textContent = 'Saved!';
        
        setTimeout(() => {
            saveStatus.textContent = '';
        }, 3000);
        
        if (!noteId && data.note) {
            // Redirect to view page after creating new note
            setTimeout(() => {
                window.location.href = `/notes/${data.note.id}`;
            }, 1000);
        }
    } catch (error) {
        showToast(error.message || 'Failed to save note', 'error');
        saveStatus.textContent = 'Failed to save';
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = noteId ? 'Update Note' : 'Save Note';
    }
}

// Auto-save (optional enhancement)
let autoSaveTimeout;
function setupAutoSave() {
    const title = document.getElementById('note-title');
    
    [title, editor].forEach(element => {
        if (element) {
            element.addEventListener('input', () => {
                clearTimeout(autoSaveTimeout);
                const saveStatus = document.getElementById('save-status');
                saveStatus.textContent = 'Unsaved changes';
                
                // Auto-save after 3 seconds of inactivity
                autoSaveTimeout = setTimeout(() => {
                    const noteId = document.getElementById('note-id').value;
                    if (noteId) {
                        saveNote();
                    }
                }, 3000);
            });
        }
    });
}

// Form Submit Handler
function setupFormHandler() {
    const form = document.getElementById('note-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            saveNote();
        });
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initEditor();
    setupFormHandler();
    // setupAutoSave(); // Uncomment to enable auto-save
});
