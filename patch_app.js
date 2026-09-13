const fs = require('fs');

const content = fs.readFileSync('web/app.js', 'utf8');

const regex = /function renderAssetGrid\(assets, container, showAnimations = true\) \{([\s\S]*?)\}\n\nfunction renderDashboard/m;

const replacement = `let currentObserver = null;

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

            const assetUrl = \`asset.html?id=\${encodeURIComponent(asset.identifier)}\`;

            const currentFlag = GLOBAL_DATA.flags[asset.identifier] || 'none';
            const isFav = currentFlag === 'favorite';
            const isErr = currentFlag === 'error';
            
            if (currentFlag !== 'none') {
                card.style.borderWidth = '2px';
                card.style.borderStyle = 'solid';
                card.style.borderColor = isFav ? '#ffca28' : '#ef5350';
            }

            card.innerHTML = \`
                <a href="\${assetUrl}" style="display:block; text-decoration: none; position: relative;">
                    \${imagesHtml}
                </a>
                <div class="card-body" style="padding: 0.75rem 1rem;">
                    <div style="font-size: 0.85rem; margin-bottom: 0.25rem; display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                        <a href="\${assetUrl}" style="color: #999999; text-decoration: none; transition: color 0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1;" onmouseover="this.style.color='#cccccc'" onmouseout="this.style.color='#999999'">\${asset.name}</a>
                        <div style="display: flex; gap: 0.5rem; font-size: 1rem; flex-shrink: 0;">
                            <button class="flag-fav" onclick="setFlag(event, '\${asset.identifier.replace(/'/g, "\\\\'")}', 'favorite')" style="background: none; border: none; cursor: pointer; color: \${isFav ? '#ffca28' : 'rgba(255,255,255,0.3)'}; padding: 0; margin: 0; transition: color 0.2s;" onmouseover="this.style.color='#ffca28'" onmouseout="if(GLOBAL_DATA.flags['\${asset.identifier.replace(/'/g, "\\\\'")}'] !== 'favorite') this.style.color='rgba(255,255,255,0.3)'">
                                <i class="fa-solid fa-star"></i>
                            </button>
                            <button class="flag-err" onclick="setFlag(event, '\${asset.identifier.replace(/'/g, "\\\\'")}', 'error')" style="background: none; border: none; cursor: pointer; color: \${isErr ? '#ef5350' : 'rgba(255,255,255,0.3)'}; padding: 0; margin: 0; transition: color 0.2s;" onmouseover="this.style.color='#ef5350'" onmouseout="if(GLOBAL_DATA.flags['\${asset.identifier.replace(/'/g, "\\\\'")}'] !== 'error') this.style.color='rgba(255,255,255,0.3)'">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                            </button>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem;">
                        <a href="vendor.html?name=\${encodeURIComponent(providerName)}" style="color: #666666; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#999999'" onmouseout="this.style.color='#666666'">\${providerName}</a>
                        <span title="\${asset.type}" style="cursor: help; color: #555555; transition: color 0.2s;" onmouseover="this.style.color='#999999'" onmouseout="this.style.color='#555555'">\${typeIcon}</span>
                    </div>
                    \${asset.visibility === 'hidden' ? '<div style="color: #e74c3c; font-size: 0.8rem; margin-top: 0.25rem;">[hidden]</div>' : ''}
                </div>
            \`;
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

function renderDashboard`;

const newContent = content.replace(regex, replacement);
fs.writeFileSync('web/app.js', newContent);
console.log("Patched web/app.js");
