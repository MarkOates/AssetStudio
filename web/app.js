let GLOBAL_DATA = null;
let animationTimers = [];

async function loadData() {
    if (GLOBAL_DATA) return GLOBAL_DATA;
    try {
        const response = await fetch('viewer_data.json');
        if (!response.ok) throw new Error("viewer_data.json not found");
        GLOBAL_DATA = await response.json();
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
            let val = Array.isArray(obj[key]) ? obj[key].join('<br>') : obj[key];
            if (val === null || val === undefined) val = 'null';
            html += `<tr><td class="key-col">${prefix}${key}</td><td class="val-col">${val}</td></tr>`;
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
        
        if (!showAnimations) {
            if (type === 'spritesheet') {
                el.style.backgroundPosition = '0px 0px';
            } else if (type === 'multifile') {
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
                el.style.backgroundPosition = `-${currentFrame * cellWidth}px 0px`;
            }, intervalMs);
            animationTimers.push(timer);
        } else if (type === 'multifile') {
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

function renderAssetGrid(assets, container, showAnimations = true) {
    container.innerHTML = '';
    
    // Filter out hidden assets if desired (or just show all for auditing)
    let visibleAssets = assets; 

    visibleAssets.forEach(asset => {
        const pack = GLOBAL_DATA.asset_packs[asset.asset_pack_id];
        const providerName = pack ? pack.provider : 'Unknown';
        
        const card = document.createElement('div');
        card.className = 'card';
        
        let imgHtml = '<div class="placeholder">Missing Mapping</div>';
        if (asset.FileMapping && asset.FileMapping.source_files && asset.FileMapping.source_files.length > 0) {
            const src = asset.FileMapping.source_files[0];
            const anim = asset.animation_profile;
            const isMissingHandler = `onerror="this.onerror=null; this.outerHTML='<div class=\\'placeholder\\' style=\\'color:#e74c3c;\\'>File Not Found</div>';"`;

            if (anim && anim.num_frames > 1) {
                if (asset.FileMapping.is_from_sprite_sheet && asset.FileMapping.cell_dimensions) {
                    const w = asset.FileMapping.cell_dimensions.width;
                    const h = asset.FileMapping.cell_dimensions.height;
                    const innerHtml = `<div class="anim-container" 
                                    data-type="spritesheet" 
                                    data-frames-count="${anim.num_frames}" 
                                    data-duration="${anim.frame_duration}"
                                    data-cell-width="${w}"
                                    style="width: ${w}px; height: ${h}px; margin: 0 auto; background-image: url('${src}'); background-repeat: no-repeat; image-rendering: pixelated; transform: scale(2); transform-origin: center;"></div>`;
                    
                    imgHtml = `<div style="height: 180px; display: flex; align-items: center; justify-content: center; background: #161616; border-bottom: 1px solid #3a3a3a; overflow:hidden;">${innerHtml}</div>`;
                } else if (!asset.FileMapping.is_from_sprite_sheet && asset.FileMapping.source_files.length > 1) {
                    const framesStr = JSON.stringify(asset.FileMapping.source_files).replace(/"/g, '&quot;');
                    imgHtml = `<div class="anim-container" 
                                    data-type="multifile" 
                                    data-frames-count="${anim.num_frames}" 
                                    data-duration="${anim.frame_duration}"
                                    data-frames="${framesStr}"
                                    style="height: 180px; display: flex; align-items: center; justify-content: center; background: #161616; border-bottom: 1px solid #3a3a3a;">
                                    <img src="${src}" alt="${asset.name}" style="max-height: 100%; max-width: 100%; object-fit: contain;" ${isMissingHandler}>
                               </div>`;
                } else {
                     imgHtml = `<img src="${src}" alt="${asset.name}" ${isMissingHandler}>`;
                }
            } else {
                imgHtml = `<img src="${src}" alt="${asset.name}" ${isMissingHandler}>`;
            }
        }

        const assetUrl = `asset.html?id=${encodeURIComponent(asset.identifier)}`;

        card.innerHTML = `
            <a href="${assetUrl}" style="display:block;">${imgHtml}</a>
            <div class="card-body">
                <h3><a href="${assetUrl}">${asset.name}</a></h3>
                <p><strong>Type:</strong> ${asset.type}</p>
                <p><strong>Provider:</strong> <a href="vendor.html?name=${encodeURIComponent(providerName)}">${providerName}</a></p>
                ${asset.visibility === 'hidden' ? '<p style="color: #e74c3c; font-size: 0.8rem;">[Hidden]</p>' : ''}
            </div>
        `;
        container.appendChild(card);
    });

    renderAnimations(showAnimations);
}
