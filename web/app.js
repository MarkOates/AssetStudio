async function setFlag(event, identifier, flagType) {
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
}
let GLOBAL_DATA = null;
let animationTimers = [];

async function openInFinder(targetPath) {
    try {
        await fetch('/api/open-finder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target: targetPath })
        });
    } catch (e) {
        console.error("Failed to open finder", e);
    }
}

async function syncData() {
    const btn = document.getElementById('sync-btn');
    if (btn) {
        btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Syncing...';
        btn.disabled = true;
    }
    
    try {
        const res = await fetch('/api/sync', { method: 'POST' });
        if (!res.ok) throw new Error("Sync failed");
        
        // Reload page to fetch new JSON
        window.location.reload();
    } catch (e) {
        console.error(e);
        if (btn) {
            btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Error';
            btn.style.background = '#e74c3c';
        }
    }
}

async function loadData() {
    if (GLOBAL_DATA) return GLOBAL_DATA;
    try {
        const response = await fetch('viewer_data.json');
        if (!response.ok) throw new Error("viewer_data.json not found");
        GLOBAL_DATA = await response.json();
        
        try {
            const flagsRes = await fetch('flags.json');
            GLOBAL_DATA.flags = flagsRes.ok ? await flagsRes.json() : {};
        } catch {
            GLOBAL_DATA.flags = {};
        }
        try {
            const notesRes = await fetch('notes.json');
            GLOBAL_DATA.notes = notesRes.ok ? await notesRes.json() : {};
        } catch {
            GLOBAL_DATA.notes = {};
        }

        
        return GLOBAL_DATA;
    } catch (e) {
        console.error("Could not load viewer_data.json.", e);
        document.body.innerHTML = "<h1>Error: Could not load viewer_data.json. Did you run the python script?</h1>";
        throw e;
    }
}

function generateTableRows(obj, prefix = '') {
    let html = '';
    for (const key in obj) {
        if (obj[key] && typeof obj[key] === 'object' && !Array.isArray(obj[key])) {
            html += generateTableRows(obj[key], prefix + key + '.');
        } else {
            let isComplex = false;
            let val = Array.isArray(obj[key]) 
                ? obj[key].map(item => {
                    if (typeof item === 'object') {
                        isComplex = true;
                        return JSON.stringify(item, null, 2);
                    }
                    return item;
                }).join('<br><br>') 
                : obj[key];
            if (val === null || val === undefined) val = 'null';
            
            if (isComplex) {
                html += `<tr><td class="key-col">${prefix}${key}</td><td class="val-col"><pre style="margin:0; white-space:pre-wrap; font-family:monospace; font-size: 0.85em;">${val}</pre></td></tr>`;
            } else {
                html += `<tr><td class="key-col">${prefix}${key}</td><td class="val-col">${val}</td></tr>`;
            }
        }
    }
    return html;
}

function stopAnimations() {
    animationTimers.forEach(clearInterval);
    animationTimers = [];
}

function renderAnimations(showAnimations) {
    stopAnimations();
    
    document.querySelectorAll('.anim-container').forEach(el => {
        const type = el.dataset.type;
        const numFrames = parseInt(el.dataset.framesCount);
        const sx = parseInt(el.dataset.startX) || 0;
        const sy = parseInt(el.dataset.startY) || 0;
        
        if (!showAnimations) {
            if (type === 'spritesheet') {
                el.style.backgroundPosition = `-${sx}px -${sy}px`;
            } else if (type === 'multi_file_animation') {
                const frames = JSON.parse(el.dataset.frames);
                el.querySelector('img').src = frames[0];
            }
            return;
        }

        const durationSec = parseFloat(el.dataset.duration) || 0.1;
        const intervalMs = durationSec * 1000;
        let currentFrame = 0;
        
        if (type === 'spritesheet') {
            const cellWidth = parseInt(el.dataset.cellWidth);
            const timer = setInterval(() => {
                currentFrame = (currentFrame + 1) % numFrames;
                const newX = sx + (currentFrame * cellWidth);
                el.style.backgroundPosition = `-${newX}px -${sy}px`;
            }, intervalMs);
            animationTimers.push(timer);
        } else if (type === 'multi_file_animation') {
            const frames = JSON.parse(el.dataset.frames);
            const img = el.querySelector('img');
            const timer = setInterval(() => {
                currentFrame = (currentFrame + 1) % numFrames;
                img.src = frames[currentFrame];
            }, intervalMs);
            animationTimers.push(timer);
        }
    });
}
function generateAssetPreviewHtml(asset, boxHeight = 180) {
    let imagesHtml = '<div class="placeholder">Missing Mapping</div>';
    
    if (asset.resource && asset.resource.source_files && asset.resource.source_files.length > 0) {
        const src = asset.resource.source_files[0];
        const anim = asset.animation_profile;
        const isMissingHandler = `onerror="this.onerror=null; this.outerHTML='<div class=\\'placeholder\\' style=\\'color:#e74c3c;\\'>File Not Found</div>';"`;

        if (anim && anim.num_frames > 1) {
            if ((asset.resource.type === 'animation_frames' || asset.resource.type === 'multi_directional_sprite') && asset.resource.cell_dimensions) {
                const w = asset.resource.cell_dimensions.width;
                const h = asset.resource.cell_dimensions.height;
                // Dynamically scale sprite to fit box height, capped at 12x
                const scale = Math.min(12, Math.max(1, Math.floor((boxHeight - 20) / h)));
                
                let renderNumFrames = anim.num_frames;
                let sx = asset.resource.start_offset ? (asset.resource.start_offset.x || 0) : 0;
                let sy = asset.resource.start_offset ? (asset.resource.start_offset.y || 0) : 0;
                
                if (asset.resource.inferred_grid) {
                    // Clamp to columns to prevent 1D overflow
                    renderNumFrames = asset.resource.inferred_grid.columns || renderNumFrames;
                    if (asset.resource.inferred_grid.inferred_animations && asset.resource.inferred_grid.inferred_animations.length > 0) {
                        const firstAnim = asset.resource.inferred_grid.inferred_animations[0];
                        sy += (firstAnim.row || 0) * h;
                    }
                }
                
                const innerHtml = `<div class="anim-container" 
                                data-type="spritesheet" 
                                data-frames-count="${renderNumFrames}" 
                                data-duration="${anim.base_frame_duration}"
                                data-cell-width="${w}"
                                data-start-x="${sx}"
                                data-start-y="${sy}"
                                style="width: ${w}px; height: ${h}px; position: absolute; top: 50%; left: 50%; background-image: url('${src}'); background-position: -${sx}px -${sy}px; background-repeat: no-repeat; image-rendering: pixelated; transform: translate(-50%, -50%) scale(${scale}); transform-origin: center;"></div>`;
                
                imagesHtml = `<div style="height: ${boxHeight}px; width: 100%; position: relative; background: #161616; overflow:hidden;">${innerHtml}</div>`;
            } else if (asset.resource.type === 'multi_file_animation' && asset.resource.source_files.length > 1) {
                const framesStr = JSON.stringify(asset.resource.source_files).replace(/"/g, '&quot;');
                imagesHtml = `<div class="anim-container" 
                                data-type="multi_file_animation" 
                                data-frames-count="${anim.num_frames}" 
                                data-duration="${anim.base_frame_duration}"
                                data-frames="${framesStr}"
                                style="height: ${boxHeight}px; width: 100%; display: flex; align-items: center; justify-content: center; background: #161616; padding: 10px; box-sizing: border-box;">
                                <img src="${src}" alt="${asset.name}" style="width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated;" ${isMissingHandler}>
                           </div>`;
            } else {
                 imagesHtml = `<div style="height: ${boxHeight}px; width: 100%; display: flex; align-items: center; justify-content: center; background: #161616; padding: 10px; box-sizing: border-box;"><img src="${src}" alt="${asset.name}" style="width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated;" ${isMissingHandler}></div>`;
            }
        } else {
            imagesHtml = `<div style="height: ${boxHeight}px; width: 100%; display: flex; align-items: center; justify-content: center; background: #161616; padding: 10px; box-sizing: border-box;"><img src="${src}" alt="${asset.name}" style="width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated;" ${isMissingHandler}></div>`;
        }
    }
    return imagesHtml;
}

let currentObserver = null;

function renderAssetGrid(assets, container, showAnimations = true) {
    container.innerHTML = '';
    
    if (currentObserver) {
        currentObserver.disconnect();
        currentObserver = null;
    }

    let visibleAssets = assets; 
    const CHUNK_SIZE = 50;
    let currentIndex = 0;

    function renderChunk() {
        const chunk = visibleAssets.slice(currentIndex, currentIndex + CHUNK_SIZE);
        if (chunk.length === 0) return;

        const oldSentinel = container.querySelector('.scroll-sentinel');
        if (oldSentinel) oldSentinel.remove();

        chunk.forEach(asset => {
            const pack = GLOBAL_DATA.asset_packs[asset.asset_pack_identifier];
            const providerName = pack ? pack.provider : 'Unknown';
            
            const card = document.createElement('div');
            card.className = 'card';
            
            let imagesHtml = generateAssetPreviewHtml(asset);
            
            let typeIcon = '<i class="fa-solid fa-file"></i>';
            if (asset.type === 'animation') typeIcon = '<i class="fa-solid fa-film" title="Animation"></i>';
            else if (asset.type === 'sprite_sheet' || asset.type === 'multi_directional_sprite') typeIcon = '<i class="fa-solid fa-border-all" title="Sprite Sheet"></i>';
            else if (asset.type === 'image' || asset.type === 'static_image') typeIcon = '<i class="fa-solid fa-image" title="Image"></i>';
            else if (asset.type === 'audio' || asset.type === 'sound_effect' || asset.type === 'music') typeIcon = '<i class="fa-solid fa-music" title="Audio"></i>';
            else if (asset.type === 'pixel_font' || asset.type === 'ttf_font') typeIcon = '<i class="fa-solid fa-font" title="Font"></i>';

            const assetUrl = `asset.html?id=${encodeURIComponent(asset.identifier)}`;

            const currentFlag = GLOBAL_DATA.flags[asset.identifier] || 'none';
            const isFav = currentFlag === 'favorite';
            const isErr = currentFlag === 'error';
            
            if (currentFlag !== 'none') {
                card.style.borderWidth = '2px';
                card.style.borderStyle = 'solid';
                card.style.borderColor = isFav ? '#ffca28' : '#ef5350';
            }

            card.innerHTML = `
                <a href="${assetUrl}" style="display:block; text-decoration: none; position: relative;">
                    ${imagesHtml}
                </a>
                <div class="card-body" style="padding: 0.75rem 1rem;">
                    <div style="font-size: 0.85rem; margin-bottom: 0.25rem; display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                        <a href="${assetUrl}" style="color: #999999; text-decoration: none; transition: color 0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1;" onmouseover="this.style.color='#cccccc'" onmouseout="this.style.color='#999999'">${asset.name}</a>
                        <div style="display: flex; gap: 0.5rem; font-size: 1rem; flex-shrink: 0;">
                            <button class="flag-fav" onclick="setFlag(event, '${asset.identifier.replace(/'/g, "\\'")}', 'favorite')" style="background: none; border: none; cursor: pointer; color: ${isFav ? '#ffca28' : 'rgba(255,255,255,0.3)'}; padding: 0; margin: 0; transition: color 0.2s;" onmouseover="this.style.color='#ffca28'" onmouseout="if(GLOBAL_DATA.flags['${asset.identifier.replace(/'/g, "\\'")}'] !== 'favorite') this.style.color='rgba(255,255,255,0.3)'">
                                <i class="fa-solid fa-star"></i>
                            </button>
                            <button class="flag-err" onclick="setFlag(event, '${asset.identifier.replace(/'/g, "\\'")}', 'error')" style="background: none; border: none; cursor: pointer; color: ${isErr ? '#ef5350' : 'rgba(255,255,255,0.3)'}; padding: 0; margin: 0; transition: color 0.2s;" onmouseover="this.style.color='#ef5350'" onmouseout="if(GLOBAL_DATA.flags['${asset.identifier.replace(/'/g, "\\'")}'] !== 'error') this.style.color='rgba(255,255,255,0.3)'">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                            </button>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem;">
                        <a href="vendor.html?name=${encodeURIComponent(providerName)}" style="color: #666666; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#999999'" onmouseout="this.style.color='#666666'">${providerName}</a>
                        <span title="${asset.type}" style="cursor: help; color: #555555; transition: color 0.2s;" onmouseover="this.style.color='#999999'" onmouseout="this.style.color='#555555'">${typeIcon}</span>
                    </div>
                    ${asset.visibility === 'hidden' ? '<div style="color: #e74c3c; font-size: 0.8rem; margin-top: 0.25rem;">[hidden]</div>' : ''}
                </div>
            `;
            container.appendChild(card);
        });

        currentIndex += CHUNK_SIZE;

        if (currentIndex < visibleAssets.length) {
            const sentinel = document.createElement('div');
            sentinel.className = 'scroll-sentinel';
            sentinel.style.width = '100%';
            sentinel.style.height = '20px';
            container.appendChild(sentinel);
            
            if (!currentObserver) {
                currentObserver = new IntersectionObserver((entries) => {
                    if (entries[0].isIntersecting) {
                        renderChunk();
                    }
                }, { rootMargin: '300px' });
            }
            currentObserver.observe(sentinel);
        }
        
        renderAnimations(showAnimations);
    }

    renderChunk();
}

function renderDashboard(errors) {
    if (!errors) errors = [];
    
    // 1. Group Errors
    const groups = {};
    errors.forEach(err => {
        if (!groups[err.type]) groups[err.type] = [];
        groups[err.type].push(err);
    });
    
    // 2. Render Stats
    const statsContainer = document.getElementById('dashboard-stats');
    let statsHtml = `
        <div class="stat-card">
            <h3>Total Discrepancies</h3>
            <div class="value" style="color: #e74c3c;">${errors.length.toLocaleString()}</div>
        </div>
    `;
    
    // Sort types by count descending
    const sortedTypes = Object.keys(groups).sort((a,b) => groups[b].length - groups[a].length);
    
    sortedTypes.forEach(type => {
        statsHtml += `
            <div class="stat-card">
                <h3>${type}</h3>
                <div class="value">${groups[type].length.toLocaleString()}</div>
            </div>
        `;
    });
    statsContainer.innerHTML = statsHtml;
    
    // 3. Render Error Tables
    const errorsContainer = document.getElementById('dashboard-errors');
    let errorsHtml = '';
    
    sortedTypes.forEach(type => {
        const errs = groups[type];
        
        let ctxKeys = [];
        if (errs.length > 0) {
            ctxKeys = Object.keys(errs[0].context);
        }
        
        let tableRows = '';
        // Limit to 1000 for DOM safety
        const limit = 1000;
        for(let i=0; i<Math.min(errs.length, limit); i++) {
            const err = errs[i];
            let rowHtml = '';
            ctxKeys.forEach(k => {
                let val = err.context[k] || '';
                
                // --- RICH DATA TREATMENTS ---
                if (k === 'pack_id' && typeof val === 'string' && val.includes('/')) {
                    const provider = val.split('/')[0];
                    val = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-family: monospace; color: #eeeeee;">${val}</span>
                            <div style="display: flex; gap: 20px; font-size: 1.1em;">
                                <a href="vendor.html?name=${encodeURIComponent(provider)}" style="color: #aaaaaa; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#eeeeee'" onmouseout="this.style.color='#aaaaaa'" title="View Vendor Page"><i class="fa-solid fa-store"></i></a>
                                <button onclick="openInFinder('${val}')" style="background: none; border: none; color: #aaaaaa; cursor: pointer; padding: 0; font-size: 1em; transition: color 0.2s;" onmouseover="this.style.color='#eeeeee'" onmouseout="this.style.color='#aaaaaa'" title="Reveal in Finder"><i class="fa-solid fa-folder-open"></i></button>
                            </div>
                        </div>`;
                } else if (k === 'identifier') {
                    val = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-family: monospace; color: #eeeeee;">${val}</span>
                            <a href="asset.html?id=${encodeURIComponent(val)}" style="color: #aaaaaa; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#eeeeee'" onmouseout="this.style.color='#aaaaaa'" title="View Asset Details"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>
                        </div>`;
                } else if (k === 'file' && err.type === 'UncataloguedFile') {
                    const fileUrl = `/Assets/${val}`;
                    const isImg = val.match(/\.(png|jpg|jpeg|gif)$/i);
                    val = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                ${isImg ? `<a href="${fileUrl}" target="_blank"><div style="width: 24px; height: 24px; background-image: url('${fileUrl}'); background-size: contain; background-repeat: no-repeat; background-position: center; border: 1px solid #444; border-radius: 3px; transition: border-color 0.2s;" onmouseover="this.style.borderColor='#888'" onmouseout="this.style.borderColor='#444'" title="Preview Image"></div></a>` : ''}
                                <span style="font-family: monospace; color: #eeeeee;">${val}</span>
                            </div>
                            <div style="display: flex; gap: 20px; font-size: 1.1em;">
                                <a href="${fileUrl}" target="_blank" style="color: #aaaaaa; transition: color 0.2s;" onmouseover="this.style.color='#eeeeee'" onmouseout="this.style.color='#aaaaaa'" title="Open in Browser"><i class="fa-solid fa-globe"></i></a>
                                <button onclick="openInFinder('${fileUrl}')" style="background: none; border: none; color: #aaaaaa; cursor: pointer; padding: 0; font-size: 1em; transition: color 0.2s;" onmouseover="this.style.color='#eeeeee'" onmouseout="this.style.color='#aaaaaa'" title="Reveal in Finder"><i class="fa-solid fa-folder-open"></i></button>
                            </div>
                        </div>
                    `;
                } else if (k === 'file') {
                    val = `<span style="font-family: monospace; color: #eeeeee;">${val}</span>`;
                }
                
                rowHtml += `<td>${val}</td>`;
            });
            tableRows += `<tr>${rowHtml}</tr>`;
        }
        
        let truncatedMsg = '';
        if (errs.length > limit) {
            truncatedMsg = `<tr><td colspan="${ctxKeys.length}" style="text-align: center; color: #a0a0a5; padding: 1rem; font-style: italic;">... and ${(errs.length - limit).toLocaleString()} more suppressed</td></tr>`;
        }
        
        const genericMessage = errs.length > 0 ? errs[0].message : '';
        const theadHtml = `<tr>${ctxKeys.map(k => `<th>${k}</th>`).join('')}</tr>`;
        
        errorsHtml += `
            <div class="error-group">
                <div class="error-group-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'block' ? 'none' : 'block'">
                    <h3>${type}</h3>
                    <div style="color: #999;">${errs.length.toLocaleString()} items &nbsp; <i class="fa-solid fa-chevron-down"></i></div>
                </div>
                <div class="error-group-content">
                    <p style="color: #bbbbbb; margin-top: 0; margin-bottom: 1.5rem; font-size: 0.95rem;">${genericMessage}</p>
                    <table class="error-table">
                        <thead>
                            ${theadHtml}
                        </thead>
                        <tbody>
                            ${tableRows}
                            ${truncatedMsg}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    });
    
    errorsContainer.innerHTML = errorsHtml;
}

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
