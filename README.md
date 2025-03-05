# GTM Auto-Update Tool

A lightweight Python tool to automatically check for and deploy updates to your Google Tag Manager (GTM) container.
This tool essentially stores a fresh version of the GTM container on your website, meaning you can serve it locally, as a 1st-party resource.

## Overview

This tool monitors your Google Tag Manager container for version changes and automatically downloads the latest version when updates are detected. It features:

- Version tracking to avoid unnecessary updates
- Automatic backups of previous versions
- Configurable backup retention
- Simple setup with minimal dependencies

## How It Works

1. Retrieves the current GTM version from a local file
2. Fetches the GTM container JavaScript directly from Google
3. Extracts the version number from the JavaScript code
4. If a new version is detected:
   - Creates a backup of the current version
   - Updates the local version file
   - Downloads the new container JavaScript
5. Maintains a configurable number of backup versions, removing older ones

## Installation

1. Clone this repository or download the files
2. Ensure you have Python 3.6+ installed
3. Update `settings.py` with your configuration details

## Configuration

Edit the `settings.py` file to match your environment:

```python
settings = {
    'container': 'GTM-XXXX',     # Your GTM container ID
    'domain': 'yoursite.com',    # Your website domain
    'path': '/path/to/assets/',  # Directory to store GTM files
    'version_file': 'gtm.version', # Filename to track version
    'number_archive': 5          # Number of backups to keep
}
```

### Configuration Options

| Option | Description |
|--------|-------------|
| `container` | Your GTM container ID (format: GTM-XXXX) |
| `domain` | Your website domain (for reference) |
| `path` | Directory where GTM files will be stored |
| `version_file` | Filename to track the current version |
| `number_archive` | Number of backup versions to retain |

## Usage

Run the script manually:

```bash
python gtm_update.py
```

For automatic updates, add it to your crontab:

```bash
# Check for GTM updates every hour
0 * * * * cd /path/to/script && python gtm_update.py
```

## File Structure

After running, your directory will contain:

```
/path/to/assets/
├── gtm.js           # Current GTM container JavaScript
├── gtm.version      # Current version number
├── gtm.js_175       # Backup of version 175
├── gtm.js_174       # Backup of version 174
└── ...
```

## Logging

The optimized version adds logging capabilities to track execution and troubleshoot issues. Logs are written to both the console and a `gtm_update.log` file.

## Optimization Benefits

The optimized script includes the following improvements:

1. **Error handling** - Gracefully handles network issues and file access problems
2. **Logging** - Detailed logs for troubleshooting and monitoring
3. **Code organization** - Modular functions for better maintainability
4. **Path handling** - Uses `os.path.join()` for better cross-platform compatibility
5. **Exit codes** - Returns appropriate exit codes for integration with automation systems
6. **Timeout handling** - Adds request timeout to prevent hanging
7. **Improved version extraction** - More robust parsing of version information

## Integration Ideas

- Add the script to your CI/CD pipeline
- Create a webhook to trigger the update when GTM publishes changes
- Expand to handle multiple GTM containers
- Add notification functionality (email, Slack, etc.) for version changes
