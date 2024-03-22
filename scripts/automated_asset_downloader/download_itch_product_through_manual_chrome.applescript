-- Usage:
-- From command-line:
-- osascript /Users/markoates/Repos/AssetStudio/scripts/automated_asset_downloader/download_itch_product_through_manual_chrome.applescript "https://ansimuz.itch.io/gothicvania-bridge-art-pack/download/bvgMYW8BM2vRsmje940VLTQO_47HNZJ7TDeTFbBH"

-- Obtain the urlArg as the first command-line
-- set urlArg to item 1 of argv

-- Open Chrome to a specific URL
tell application "Google Chrome"
    activate
    open location "https://ansimuz.itch.io/gothicvania-bridge-art-pack/download/bvgMYW8BM2vRsmje940VLTQO_47HNZJ7TDeTFbBH"
    -- open location urlArg
end tell

repeat
    tell application "Google Chrome"
        set isLoading to loading of front window's active tab
    end tell
    if not isLoading then exit repeat
    delay 1
end repeat

-- Count the number of buttons with the text "Download"
tell application "Google Chrome"
    set downloadCount to execute front window's active tab javascript "document.querySelectorAll('.uploads .upload').length;"

    -- Get the names of each item
    set downloadNamesList to {}
    repeat with downloadNum from 0 to (downloadCount - 1)
      set downloadName to execute front window's active tab javascript "document.querySelectorAll('.uploads .upload')[" & downloadNum & "].querySelectorAll('.upload_name .name')[0].title"
      if downloadName is not missing value then
          set end of downloadNamesList to downloadName
      end if
    end repeat

    -- Collect the names into a string
    set downloadNamesString to ""
    repeat with i from 1 to count of downloadNamesList
        set downloadNamesString to downloadNamesString & "  - " & item i of downloadNamesList & return
    end repeat

    display alert "" & downloadCount & " downloads are available on this page." message "Press OK to start automated download (and please wait until finished)." & return & return & "Items to download:" & return & downloadNamesString buttons {"OK"}
end tell

-- if downloadCount > 0 then
    -- tell application "Google Chrome"
        -- repeat with downloadNum from 0 to (downloadCount - 1)
          -- execute front window's active tab javascript "document.querySelectorAll('.uploads .upload .button')[" & downloadNum & "].click();"
          -- delay 2
        -- end repeat
    -- end tell
-- else
    -- display dialog "No buttons with the text 'Download' found."
-- end if


-- display alert "Download process is finished." message "Writing file." buttons {"OK"}

-- Write downloadCount to a text file
-- set desktopPath to (path to desktop as text)
-- set filePath to desktopPath & "download_count.txt"
-- set fileHandle to open for access file filePath with write permission
-- set downloadCountString to downloadCount as text -- Coerce downloadCount to text
-- write downloadCountString to fileHandle
-- close access fileHandle


display alert "Download process is finished." message "Writing file." buttons {"OK"}

