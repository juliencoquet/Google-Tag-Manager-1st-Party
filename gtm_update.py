import os
import urllib.request
import logging
import sys
import re
from datetime import datetime

# Import settings from settings.py
from settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gtm_update.log"),
        logging.StreamHandler()
    ]
)

def get_current_version():
    """Get the currently stored version number."""
    version_file = os.path.join(settings['path'], settings['version_file'])
    try:
        if os.path.isfile(version_file):
            with open(version_file, 'r') as f:
                current_version = f.read().strip()
                logging.info(f"Current version: {current_version}")
                return current_version
        else:
            logging.info("No version file found, assuming initial setup")
            return "0"
    except Exception as e:
        logging.error(f"Error reading current version: {e}")
        return "0"

def get_remote_version():
    """Fetch the latest version from the GTM container."""
    try:
        url = 'https://www.googletagmanager.com/gtm.js?id=' + settings['container']
        logging.info(f"Fetching GTM container from: {url}")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            
            # Look for version in the JavaScript
            for line in data.splitlines():
                if b'"version":' in line:
                    try:
                        remote_version = line.decode('utf-8').split('"')[3]
                        logging.info(f"Found remote version: {remote_version}")
                        return remote_version, data
                    except (IndexError, UnicodeDecodeError) as e:
                        logging.warning(f"Error parsing version string: {e}")
                        break
            
            # If we didn't find the version, log it but return the data anyway
            # with a timestamp as the version
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            logging.warning(f"Could not extract version number, using timestamp: {timestamp}")
            return timestamp, data
            
    except Exception as e:
        logging.error(f"Error fetching remote version: {e}")
        return None, None

def backup_container(current_version, data):
    """Create a backup of the current GTM container."""
    try:
        backup_file = os.path.join(settings['path'], f"gtm.js_{current_version}")
        with open(backup_file, 'wb') as f:
            f.write(data)
        logging.info(f"Created backup: {backup_file}")
        return True
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        return False

def update_files(remote_version, data):
    """Update the version file and GTM container."""
    try:
        # Ensure directory exists
        os.makedirs(settings['path'], exist_ok=True)
        
        # Update the version file
        version_file = os.path.join(settings['path'], settings['version_file'])
        with open(version_file, 'w') as f:
            f.write(remote_version)
        
        # Update the GTM container
        with open(os.path.join(settings['path'], 'gtm.js'), 'wb') as f:
            f.write(data)
            
        logging.info(f"Updated to version {remote_version}")
        return True
    except Exception as e:
        logging.error(f"Error updating files: {e}")
        return False

def cleanup_backups():
    """Clean up old backup files, keeping only the latest N versions."""
    try:
        backup_files = [f for f in os.listdir(settings['path']) if f.startswith('gtm.js_')]
        backup_files.sort(reverse=True)
        
        # Keep only the latest N backups
        files_to_remove = backup_files[settings['number_archive']:]
        for filename in files_to_remove:
            file_path = os.path.join(settings['path'], filename)
            os.remove(file_path)
            logging.info(f"Removed old backup: {file_path}")
            
        return True
    except Exception as e:
        logging.error(f"Error during backup cleanup: {e}")
        return False

def main():
    """Main function to update GTM container if needed."""
    logging.info("Starting GTM update process")
    
    # Get current version
    current_version = get_current_version()
    
    # Get remote version
    remote_version, data = get_remote_version()
    if not remote_version or not data:
        logging.error("Failed to retrieve remote version, exiting")
        return 1
    
    # If versions match, no update needed
    if remote_version == current_version:
        logging.info("Already at the latest version, no update needed")
        return 0
    
    # Versions differ, update needed
    logging.info(f"Version change detected: {current_version} → {remote_version}")
    
    # Backup current container
    if not backup_container(current_version, data):
        logging.warning("Failed to create backup, but continuing with update")
    
    # Update files
    if not update_files(remote_version, data):
        logging.error("Failed to update files")
        return 1
    
    # Clean up old backups
    if not cleanup_backups():
        logging.warning("Failed to clean up old backups")
    
    logging.info("GTM update completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())