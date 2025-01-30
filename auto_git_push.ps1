$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "F:\FYP-Docs\docs"
$watcher.Filter = "*.*"  # Watch all file types
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

# Define the action when a file is changed
$action = {
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c cd /d F:\FYP-Docs\docs && git add . && git commit -m `"Auto commit: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`" && git push" -NoNewWindow -Wait
}

# Event handlers for different types of changes
Register-ObjectEvent $watcher "Created" -Action $action
Register-ObjectEvent $watcher "Changed" -Action $action
Register-ObjectEvent $watcher "Deleted" -Action $action

# Keep the script running
while ($true) { Start-Sleep 5 }
