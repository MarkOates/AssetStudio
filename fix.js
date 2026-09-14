const fs = require('fs');
let code = fs.readFileSync('web/app.js', 'utf8');
code = code.replace(/async function setFlag[\s\S]*?console\.error\("Failed to set flag", e\);\n    \}\n\}/, 
`async function setFlag(event, identifier, flagType) {
    event.preventDefault();
    event.stopPropagation();
    
    // Toggle logic: if clicking the same flag, remove it.
    if (GLOBAL_DATA.flags[identifier] === flagType) {
        flagType = 'none';
    }
    
    GLOBAL_DATA.flags[identifier] = (flagType === 'none') ? undefined : flagType;
    
    const container = event.currentTarget.closest('.card, .show-page-header');
    
    try {
        await fetch('/api/flag', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({identifier, flag_type: flagType})
        });
        
        // Update DOM visual state
        if (container) {
            const favBtn = container.querySelector('.flag-fav');
            const errBtn = container.querySelector('.flag-err');
            if (favBtn) favBtn.style.color = (flagType === 'favorite') ? '#ffca28' : 'rgba(255,255,255,0.3)';
            if (errBtn) errBtn.style.color = (flagType === 'error') ? '#ef5350' : 'rgba(255,255,255,0.3)';
            
            // Add or remove colored border only if it's a grid card
            if (container.classList.contains('card')) {
                if (flagType !== 'none') {
                    container.style.borderColor = (flagType === 'favorite') ? '#ffca28' : '#ef5350';
                    container.style.borderWidth = '2px';
                    container.style.borderStyle = 'solid';
                } else {
                    container.style.borderColor = '';
                    container.style.borderWidth = '';
                    container.style.borderStyle = '';
                }
            }
        }
    } catch (e) {
        console.error("Failed to set flag:", e);
    }
}`);
fs.writeFileSync('web/app.js', code);
