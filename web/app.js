// MOCK_DATA removed, loading entirely from JSON now.
let GLOBAL_DATA = null;

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

function renderAssetGrid(assets, container) {
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
            // Using onerror to replace broken image paths (like typos in the CSV) with a clean placeholder
            // so they don't mush up the UI layout.
            const src = asset.FileMapping.source_files[0];
            imgHtml = `<img src="${src}" alt="${asset.name}" onerror="this.onerror=null; this.outerHTML='<div class=\\'placeholder\\' style=\\'color:#e74c3c;\\'>File Not Found</div>';">`;
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
}
