import os
import subprocess
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set variables
REPO_PATH = r"F:\FYP-Docs"  # Change this to your repo path
COMMIT_MESSAGE = f"Automated commit on {datetime.now()}"
BRANCH = "master"  # Change if using a different branch
GITHUB_USER = "AashutoshDL"  # Your GitHub username
GITHUB_TOKEN = "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"  # Your GitHub PAT

# Function to commit and push changes
def push_changes():
    # Navigate to the repository
    os.chdir(REPO_PATH)

    # Check if there are any changes
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    
    if status.stdout.strip():
        print("Changes detected. Committing and pushing...")

        # Add all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)

        # Push changes with PAT authentication
        push_command = [
            "git", "push", f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/fyp-documents.git", BRANCH
        ]
        subprocess.run(push_command, check=True)

        print("Changes pushed successfully!")
    else:
        print("No changes to commit.")

# Watchdog event handler class
class GitChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Trigger push_changes when a file is added or modified
        if event.is_directory:  # Skip directory changes
            return
        print(f"File changed: {event.src_path}")
        push_changes()

# Set up the observer to watch the repository folder
observer = Observer()
handler = GitChangeHandler()
observer.schedule(handler, REPO_PATH, recursive=True)

# Start observing the directory
observer.start()

try:
    while True:
        time.sleep(1)  # Keeps the script running
except KeyboardInterrupt:
    observer.stop()
    print("Script stopped.")
observer.join()