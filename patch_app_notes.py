content = open('web/app.js').read()

notes_fetch = """
        try {
            const notesRes = await fetch('notes.json');
            GLOBAL_DATA.notes = notesRes.ok ? await notesRes.json() : {};
        } catch {
            GLOBAL_DATA.notes = {};
        }
"""
content = content.replace('GLOBAL_DATA.flags = {};\n        }', 'GLOBAL_DATA.flags = {};\n        }' + notes_fetch)

save_note_func = """
async function saveNote(identifier) {
    const textarea = document.getElementById('user-note-input');
    if (!textarea) return;
    const note = textarea.value;
    const btn = document.getElementById('save-note-btn');
    
    try {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        await fetch('/api/note', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({identifier, note})
        });
        GLOBAL_DATA.notes[identifier] = note;
        btn.innerHTML = '<i class="fa-solid fa-check"></i>';
        setTimeout(() => { btn.innerHTML = 'Save Note'; }, 2000);
    } catch (e) {
        console.error("Failed to save note:", e);
        btn.innerHTML = '<i class="fa-solid fa-xmark"></i> Error';
    }
}
"""
content += save_note_func

with open('web/app.js', 'w') as f:
    f.write(content)
print("Patched app.js for notes")
