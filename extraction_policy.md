# Extraction Policy

When extracting asset archives (e.g., `.zip`, `.rar`, `.7z`) within the `AssetStudio` workflow, the following policies must be adhered to in order to ensure data integrity and consistent file paths.

### 1. Data Integrity and Read-Only Restrictions
* **Source Archives Path**: All pack archive files are located in `/Users/markoates/Assets/`.
* **Source Archives**: The original archive files and their parent provider/pack directories must not be mutated, overwritten, or deleted under any circumstances.
* **Read-Only Analysis**: Automated tasks (e.g., analysis, scraping, snapshotting) within the `/Users/markoates/Assets/` directory must strictly execute using read-only operations. Modifications are only permitted during an explicit extraction task.

### 2. The `extracted/` Directory
* All contents of an archive must be extracted into a subfolder named exactly `extracted/` located at the root of the individual pack's directory.
* A metadata file named `.extractor` should be created inside the `extracted/` folder containing the string `automation` (if performed by a script or agent) so the UI accurately attributes the extraction source.

### 3. Flat Extraction
* Archives must be extracted directly into the `extracted/` folder.
* Do not create an intermediate folder named after the archive.
* If the original archive contains a top-level directory inherently, it should extract naturally. Do not artificially wrap the contents in a new directory.
* **Loose Files**: If a pack contains non-archive loose files, they must be copied into the `extracted/` folder (with the exception of `download_log.txt`). The original loose files in the parent directory must remain sacred and read-only.

### 4. Pack Schema & Extraction Properties
The `packs.json` database manages the extraction state of every pack. Agents must understand how these fields are populated:
* `extraction_folder_exists` (Read-only boolean): Dynamically computed by checking if the `extracted/` folder exists.
* `extraction_status` (Writeable string): The extracting agent must update this to `"extracted"` upon successful extraction.
* `multiple_archive_files_would_clobber_results` (Read-only boolean): Dynamically computed by checking the snapshot for file name collisions between multiple archives in the same pack.
* `has_pack_drift` (Read-only boolean): Dynamically computed by checking if the expected number of files in `download_log.txt` matches the actual physical count.
* `has_missing_log_file` (Read-only boolean): Dynamically computed by checking if the `download_log.txt` file exists.
* `can_be_extracted_by_automation` (Read-only boolean): **The absolute source of truth for extraction permissibility.** Evaluated dynamically; true only if the pack is unextracted, poses no clobber risk, has no PackDrift, and is not missing a log file. Agents and automation scripts must strictly respect this flag before initiating any extraction.
* `extractor` (Writeable string): The extracting agent must update the `extractor` property in `packs.json` to its identifier (e.g., `automated`).
* `extracted_at` (Writeable timestamp): The extracting agent must update the `extracted_at` property in `packs.json` to the current ISO 8601 timestamp.
* **Concurrency Requirement**: When updating `packs.json`, the writing process must use strict file locking to prevent race conditions, as multiple background jobs may be extracting and updating the database concurrently.


