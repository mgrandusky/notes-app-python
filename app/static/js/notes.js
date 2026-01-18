// Notes List Management
let currentFilters = {
    search: '',
    tag: '',
    sort: 'updated_at',
    order: 'desc',
    archived: false
};

let deleteNoteId = null;

// Load Notes
async function loadNotes() {
    const loading = document.getElementById('loading');
    const notesGrid = document.getElementById('notes-grid');
    const emptyState = document.getElementById('empty-state');
    
    loading.style.display = 'block';
    notesGrid.innerHTML = '';
    emptyState.style.display = 'none';
    
    try {
        const params = new URLSearchParams(currentFilters);
        const data = await apiRequest(`/api/notes?${params}`);
        
        loading.style.display = 'none';
        
        if (data.notes && data.notes.length > 0) {
            renderNotes(data.notes);
        } else {
            emptyState.style.display = 'block';
        }
    } catch (error) {
        loading.style.display = 'none';
        showToast('Failed to load notes', 'error');
    }
}

// Render Notes
function renderNotes(notes) {
    const notesGrid = document.getElementById('notes-grid');
    notesGrid.innerHTML = '';
    
    notes.forEach(note => {
        const noteCard = createNoteCard(note);
        notesGrid.appendChild(noteCard);
    });
}

// Create Note Card
function createNoteCard(note) {
    const card = document.createElement('div');
    card.className = 'note-card';
    card.onclick = () => window.location.href = `/notes/${note.id}`;
    
    const title = document.createElement('h3');
    title.className = 'note-card-title';
    title.textContent = note.title;
    
    const preview = document.createElement('div');
    preview.className = 'note-card-preview';
    preview.textContent = truncateText(note.content || '', 100);
    
    const meta = document.createElement('div');
    meta.className = 'note-card-meta';
    
    const date = document.createElement('span');
    date.textContent = formatDate(note.updated_at);
    
    const actions = document.createElement('div');
    actions.className = 'note-card-actions';
    actions.onclick = (e) => e.stopPropagation();
    
    const editBtn = document.createElement('button');
    editBtn.textContent = '✏️';
    editBtn.title = 'Edit';
    editBtn.onclick = () => window.location.href = `/notes/${note.id}/edit`;
    
    const archiveBtn = document.createElement('button');
    archiveBtn.textContent = note.is_archived ? '📂' : '📦';
    archiveBtn.title = note.is_archived ? 'Unarchive' : 'Archive';
    archiveBtn.onclick = () => archiveNote(note.id, !note.is_archived);
    
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = '🗑️';
    deleteBtn.title = 'Delete';
    deleteBtn.onclick = () => openDeleteModal(note.id);
    
    actions.appendChild(editBtn);
    actions.appendChild(archiveBtn);
    actions.appendChild(deleteBtn);
    
    meta.appendChild(date);
    meta.appendChild(actions);
    
    card.appendChild(title);
    card.appendChild(preview);
    
    if (note.tags && note.tags.length > 0) {
        const tagsDiv = document.createElement('div');
        tagsDiv.className = 'note-tags';
        note.tags.forEach(tag => {
            const tagSpan = document.createElement('span');
            tagSpan.className = 'tag';
            tagSpan.textContent = tag;
            tagsDiv.appendChild(tagSpan);
        });
        card.appendChild(tagsDiv);
    }
    
    card.appendChild(meta);
    
    return card;
}

// Archive/Unarchive Note
async function archiveNote(noteId, archived) {
    try {
        await apiRequest(`/api/notes/${noteId}/archive`, {
            method: 'POST',
            body: JSON.stringify({ archived })
        });
        
        showToast(`Note ${archived ? 'archived' : 'unarchived'} successfully`, 'success');
        loadNotes();
    } catch (error) {
        showToast('Failed to archive note', 'error');
    }
}

// Delete Note Modal
function openDeleteModal(noteId) {
    deleteNoteId = noteId;
    document.getElementById('delete-modal').style.display = 'flex';
}

function closeDeleteModal() {
    deleteNoteId = null;
    document.getElementById('delete-modal').style.display = 'none';
}

async function confirmDelete() {
    if (!deleteNoteId) return;
    
    try {
        await apiRequest(`/api/notes/${deleteNoteId}`, {
            method: 'DELETE'
        });
        
        showToast('Note deleted successfully', 'success');
        closeDeleteModal();
        loadNotes();
    } catch (error) {
        showToast('Failed to delete note', 'error');
    }
}

// Load Tags
async function loadTags() {
    try {
        const data = await apiRequest('/api/tags');
        
        if (data.tags && data.tags.length > 0) {
            renderTagFilters(data.tags);
        }
    } catch (error) {
        console.error('Failed to load tags:', error);
    }
}

// Render Tag Filters
function renderTagFilters(tags) {
    const tagsFilter = document.getElementById('tags-filter');
    
    tags.forEach(tag => {
        const btn = document.createElement('button');
        btn.className = 'tag-filter';
        btn.textContent = tag;
        btn.dataset.tag = tag;
        btn.onclick = () => filterByTag(tag);
        tagsFilter.appendChild(btn);
    });
}

// Filter by Tag
function filterByTag(tag) {
    currentFilters.tag = currentFilters.tag === tag ? '' : tag;
    
    document.querySelectorAll('.tag-filter').forEach(btn => {
        if (btn.dataset.tag === tag) {
            btn.classList.toggle('active');
        } else if (btn.dataset.tag === '') {
            btn.classList.toggle('active', currentFilters.tag === '');
        } else {
            btn.classList.remove('active');
        }
    });
    
    loadNotes();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Search
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                currentFilters.search = e.target.value;
                loadNotes();
            }, 500);
        });
    }
    
    // Sort
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            currentFilters.sort = e.target.value;
            loadNotes();
        });
    }
    
    // Order
    const orderSelect = document.getElementById('order-select');
    if (orderSelect) {
        orderSelect.addEventListener('change', (e) => {
            currentFilters.order = e.target.value;
            loadNotes();
        });
    }
    
    // Archived Toggle
    const archivedToggle = document.getElementById('archived-toggle');
    if (archivedToggle) {
        archivedToggle.addEventListener('change', (e) => {
            currentFilters.archived = e.target.checked;
            loadNotes();
        });
    }
    
    // Initial Load
    loadNotes();
    loadTags();
});
