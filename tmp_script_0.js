
        document.addEventListener("DOMContentLoaded", () => {
            loadData().then(async data => {
                let packsData = {};
                try {
                    const res = await fetch('packs.json');
                    if (res.ok) packsData = await res.json();
                } catch(e) {
                    console.log("No packs.json found yet.");
                }

                const urlParams = new URLSearchParams(window.location.search);
                const packId = urlParams.get('id');
                const toggleContainer = document.getElementById('hidden-toggle-container');
                const toggleHidden = document.getElementById('show-hidden-toggle');
                const toggleAnim = document.getElementById('show-animations-toggle');
                
                if (packId) {
                    const packDetails = data.asset_packs[packId] || Object.values(packsData).find(p => p.provider + '/' + p.name === packId) || { name: packId };
                    
                    const tempCombined = { ...(packDetails || {}), ...(packsData[packId] || {}) };
                    const packIdentifier = tempCombined.identifier || packId;
                    
                    const combinedPackData = { identifier: packIdentifier, ...tempCombined };
                    
                    document.getElementById('pack-title').style.display = 'none';
                    
                    const imgHtml = combinedPackData.social_share_image_path 
                        ? `<img src="${combinedPackData.social_share_image_path}" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 4px;">`
                        : `<div style="color: #aaaaaa;">No Image Available</div>`;
                        
                    const showPageHtml = `
                        <div class="show-page-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                            <h2 style="margin: 0;">Pack: ${packIdentifier}</h2>
                            <a href="${combinedPackData.source_url || '#'}" target="_blank" class="nav-btn" style="text-decoration: none; padding: 6px 12px; border: 1px solid #3a3a3a; border-radius: 4px; display: inline-flex; align-items: center; gap: 8px; font-size: 0.9rem; margin: 0;">
                                <i class="fa-solid fa-arrow-up-right-from-square"></i> Original Page
                            </a>
                        </div>
                        
                        <div style="display: flex; gap: 2rem; margin-bottom: 2rem; align-items: stretch;">
                            <!-- Left Column: Large Preview -->
                            <div style="flex: 0 0 350px; border-radius: 5px; overflow: hidden; border: 1px solid #3a3a3a; background: #161616; display: flex; align-items: center; justify-content: center; min-height: 200px; max-height: 300px;">
                                ${imgHtml}
                            </div>
                            
                            <!-- Right Column: Metadata -->
                            <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 0.85rem; font-size: 1.05rem;">
                                <div><strong style="color: #aaaaaa; display: inline-block; width: 150px;">Provider:</strong> <a href="vendor.html?name=${encodeURIComponent(combinedPackData.provider || '')}" style="color: #eeeeee; text-decoration: none;">${combinedPackData.provider || 'Unknown'}</a></div>
                                <div><strong style="color: #aaaaaa; display: inline-block; width: 150px;">Extraction Status:</strong> <span style="color: ${combinedPackData.extraction_status === 'extracted' ? '#2ecc71' : '#e74c3c'}">${combinedPackData.extraction_status || 'Unknown'}</span></div>
                                <div><strong style="color: #aaaaaa; display: inline-block; width: 150px;">Clobber Risk:</strong> <span style="color: ${combinedPackData.multiple_archive_files_would_clobber_results ? '#e74c3c' : '#eeeeee'}">${combinedPackData.multiple_archive_files_would_clobber_results ? 'Yes' : 'No'}</span></div>
                                <div><strong style="color: #aaaaaa; display: inline-block; width: 150px;">Pack Drift:</strong> <span style="color: ${combinedPackData.has_pack_drift ? '#e74c3c' : '#eeeeee'}">${combinedPackData.has_pack_drift ? 'Yes' : 'No'}</span></div>
                                <div><strong style="color: #aaaaaa; display: inline-block; width: 150px;">Can Automate:</strong> <span style="color: ${combinedPackData.can_be_extracted_by_automation ? '#2ecc71' : '#eeeeee'}">${combinedPackData.can_be_extracted_by_automation ? 'Yes' : 'No'}</span></div>
                            </div>
                        </div>
                    `;
                    document.getElementById('pack-title').parentElement.insertAdjacentHTML('beforebegin', showPageHtml);
                    
                    document.getElementById('asset-grid').style.display = 'grid';
                    toggleContainer.style.display = 'flex';
                    toggleContainer.style.marginLeft = 'auto';
                    const rawDataHtml = `
                        <h3 style="margin-top: 2rem;">Raw Data:</h3>
                        <table class="data-table">
                            <tbody>
                                ${generateTableRows(combinedPackData)}
                            </tbody>
                        </table>
                    `;
                    // We'll append this after setting up the grid, or insert it after the main container.
                    
                    const packAssets = data.assets.filter(a => a.asset_pack_id === packId);
                    
                    let clobberInfoHtml = '';
                    if (packsData[packId]?.clobbered_files) {
                        const clobbered = packsData[packId].clobbered_files;
                        let clobberList = '<ul style="font-size: 0.9em; color: #ff9800; background: #2a2a2a; padding: 10px; border-radius: 4px; margin-top: 10px;">';
                        for (const [file, archives] of Object.entries(clobbered)) {
                            clobberList += `<li style="margin-bottom: 4px; margin-left: 20px;"><strong>${file}</strong> is found in: ${archives.join(', ')}</li>`;
                        }
                        clobberList += '</ul>';
                        clobberInfoHtml = `<div id="clobber-info" style="margin-bottom: 20px;"><p style="color: #f44336; font-weight: bold;">Warning: Extracting multiple archives in this pack flatly would cause file clobbering!</p>${clobberList}</div>`;
                        document.getElementById('asset-grid').insertAdjacentHTML('beforebegin', clobberInfoHtml);
                    }
                    
                    if (packAssets.length === 0) {
                        document.getElementById('asset-grid').innerHTML = `<p style="grid-column: 1/-1;">No mapped assets found for this pack. Note: This pack may need to be processed.</p>`;
                    } else {
                        function updateGrid() {
                            const showHidden = toggleHidden.checked;
                            const showAnim = toggleAnim.checked;
                            const filtered = packAssets.filter(a => showHidden || a.visibility !== 'hidden');
                            renderAssetGrid(filtered, document.getElementById('asset-grid'), showAnim);
                        }
                        
                        toggleHidden.addEventListener('change', updateGrid);
                        toggleAnim.addEventListener('change', () => renderAnimations(toggleAnim.checked));
                        updateGrid(); // Initial render
                    }
                    
                    document.getElementById('asset-grid').insertAdjacentHTML('afterend', rawDataHtml);
                } else {
                    // Show list of packs
                    const list = document.getElementById('pack-list');
                    const filters = document.getElementById('status-filters');
                    
                    // Combine packs from viewer_data and packs.json
                    const allPacks = new Map();
                    Object.keys(data.asset_packs).forEach(id => {
                        allPacks.set(id, { ...data.asset_packs[id], id, source: 'catalog' });
                    });
                    Object.keys(packsData).forEach(id => {
                        if (!allPacks.has(id)) {
                            allPacks.set(id, { ...packsData[id], id, source: 'json' });
                        } else {
                            const existing = allPacks.get(id);
                            existing.extraction_status = packsData[id].extraction_status;
                            existing.extraction_folder_exists = packsData[id].extraction_folder_exists;
                            existing.multiple_archive_files_would_clobber_results = packsData[id].multiple_archive_files_would_clobber_results;
                            existing.has_pack_drift = packsData[id].has_pack_drift;
                            existing.clobbered_files = packsData[id].clobbered_files;
                            existing.can_be_extracted_by_automation = packsData[id].can_be_extracted_by_automation;
                            existing.extractor = packsData[id].extractor;
                            existing.extracted_at = packsData[id].extracted_at;
                            existing.identifier = packsData[id].identifier;
                            existing.social_share_image_exists = packsData[id].social_share_image_exists;
                        }
                    });

                    if (Object.keys(packsData).length > 0) {
                        filters.style.display = 'block';
                    }
                    
                    const renderPackList = () => {
                        let html = `
                            <table class="data-table" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
                                <thead>
                                    <tr style="background: #252525; border-bottom: 2px solid #3a3a3a; text-align: left;">
                                        <th style="padding: 10px;">Identifier</th>
                                        <th style="padding: 10px; width: 150px;">Status</th>
                                        <th style="padding: 10px; width: 120px;">Pack Drift</th>
                                        <th style="padding: 10px; width: 150px;">Automateable</th>
                                    </tr>
                                </thead>
                                <tbody>
                        `;
                        
                        const filterAll = document.getElementById('filter-all').checked;
                        const filterExtracted = document.getElementById('filter-extracted').checked;
                        const filterUnextracted = document.getElementById('filter-unextracted').checked;
                        const filterClobber = document.getElementById('filter-clobber').checked;

                        const sortedPacks = Array.from(allPacks.values()).sort((a, b) => {
                            const aName = a.identifier || a.id;
                            const bName = b.identifier || b.id;
                            return aName.localeCompare(bName);
                        });

                        let visibleIndex = 0;
                        sortedPacks.forEach(p => {
                            const isExtracted = p.extraction_status === 'extracted';
                            const isClobber = p.multiple_archive_files_would_clobber_results;
                            const isUnextracted = !isExtracted;
                            const statusDisplay = isClobber ? "Clobber Risk" : (isExtracted ? "Extracted" : "Unextracted");
                            
                            if (!filterAll) {
                                const showExtracted = filterExtracted && isExtracted;
                                const showUnextracted = filterUnextracted && isUnextracted && !isClobber;
                                const showClobber = filterClobber && isClobber;
                                if (!showExtracted && !showUnextracted && !showClobber) return;
                            }
                            
                            const bg = (visibleIndex % 2 === 0) ? '#1e1e1e' : '#242424';
                            visibleIndex++;
                            
                            let statusColor = '#fff';
                            if (isClobber) statusColor = '#f44336';
                            else if (isExtracted) statusColor = '#4caf50';
                            
                            const hasDrift = p.has_pack_drift ? '<span style="color: #f44336;">Yes</span>' : '<span style="color: #aaaaaa;">No</span>';
                            const canAutomate = p.can_be_extracted_by_automation ? '<span style="color: #4caf50;">Yes</span>' : '<span style="color: #aaaaaa;">No</span>';
                            
                            html += `
                                <tr style="background: ${bg}; border-bottom: 1px solid #2a2a2a; transition: background 0.2s;" onmouseover="this.style.background='#2a2a2a'" onmouseout="this.style.background='${bg}'">
                                    <td style="padding: 10px;"><a href="pack.html?id=${encodeURIComponent(p.id)}" style="color: #3498db; text-decoration: none; display: block;">${p.identifier || p.id}</a></td>
                                    <td style="padding: 10px; color: ${statusColor};">${statusDisplay}</td>
                                    <td style="padding: 10px;">${hasDrift}</td>
                                    <td style="padding: 10px;">${canAutomate}</td>
                                </tr>
                            `;
                        });
                        
                        html += `</tbody></table>`;
                        list.innerHTML = html;
                    }

                    document.getElementById('filter-all').addEventListener('change', (e) => {
                        if (e.target.checked) {
                            document.getElementById('filter-extracted').checked = false;
                            document.getElementById('filter-unextracted').checked = false;
                            document.getElementById('filter-clobber').checked = false;
                        } else {
                            e.target.checked = true; // Prevent unchecking if others are false
                        }
                        renderPackList();
                    });
                    
                    const handleFilter = (e) => {
                        if (e.target.checked) {
                            document.getElementById('filter-all').checked = false;
                        }
                        if (!document.getElementById('filter-extracted').checked && !document.getElementById('filter-unextracted').checked && !document.getElementById('filter-clobber').checked) {
                            document.getElementById('filter-all').checked = true;
                        }
                        renderPackList();
                    };

                    document.getElementById('filter-extracted').addEventListener('change', handleFilter);
                    document.getElementById('filter-unextracted').addEventListener('change', handleFilter);
                    document.getElementById('filter-clobber').addEventListener('change', handleFilter);

                    renderPackList();
                }
            });
        });
    