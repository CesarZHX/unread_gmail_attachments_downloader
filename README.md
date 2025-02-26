# Unread Gmail Attachments Downloader

## Description

This script listens for unread emails in a Gmail inbox and downloads any attachments, marking the emails as read afterward. It is useful for automating attachment retrieval from Gmail.

## Requirements

- Python 3.12+
- `ezgmail` library (GPL-3.0 license)

## Installation

1. Install dependencies:

    ```sh
    pip install .
    ```

2. Obtain Google OAuth 2.0 credentials:
   - Create a new OAuth 2.0 client ID from [Google Cloud Console](https://console.cloud.google.com/)
   - Download the `client_secret.json` file (OAuth 2.0 client credentials) and place it in the root directory of the project.

## Usage

```sh
python main.py
```

### Expected Directory Structure

```text
.
├── client_secret.json  # OAuth 2.0 client credentials
├── token.json          # OAuth token file (auto-generated after first login)
├── .attachments        # Auto-generated directory where email attachments are stored
├── main.py             # Main script
├── pyproject.toml      # Project configuration for dependency management
└── README.md           # This file
```

## License

This project includes `ezgmail`, which is licensed under the GPL-3.0 license. Make sure your project complies with GPL-3.0 terms before using or redistributing this code.

## Disclaimer

This script requires access to Gmail and Google OAuth credentials. Handle your credentials securely and avoid sharing them publicly.
