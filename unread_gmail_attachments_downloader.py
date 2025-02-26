from typing import Iterable
from pathlib import Path
from time import sleep

from google.auth.exceptions import RefreshError
from ezgmail import init, unread  # type: ignore

FILE_PATH = Path(__file__)
PARENT_PATH = FILE_PATH.parent

CREDENTIALS_JSON_FILE_PATH = next(PARENT_PATH.glob("client_secret*.json"))
TOKEN_JSON_FILE_PATH = PARENT_PATH / "token.json"
ATTACHMENTS_DIR = PARENT_PATH / ".attachments"

ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)

def listen_unread_attachments(creds_file: Path, token_file: Path,
    storage_dir: Path, filter_suffixes: Iterable[str] = tuple()):
    """Listens for unread emails and downloads attachments."""
    while True:
        if not login(creds_file, token_file):
            continue
        print("📧 Listening unread email attachment")
        download_unread_attachments_continuously(storage_dir, filter_suffixes)
        print("📧 Unread email attachment listening stopped")

def download_unread_attachments_continuously(storage_dir: Path,
    filter_suffixes: Iterable[str] = tuple(), resting_seconds: int = 60):
    """Downloads attachments from unread emails and marks them as read."""
    try:
        while True:
            print("📧 Checking for new emails...")
            download_unread_attachments(storage_dir, filter_suffixes)
            print(f"📧 Waiting {resting_seconds} seconds for new emails...")
            sleep(resting_seconds)
    except Exception as error:
        print(f"📧 Error: {error}")
        raise error

def download_unread_attachments(storage_dir: Path, filter_suffixes: Iterable[str] = tuple()) -> None:
    """Downloads attachments from unread emails and marks them as read."""
    for thread in unread():
        for message in thread.messages:
            for attachment in message.attachments:
                file = storage_dir / str(message.threadId) / str(attachment)
                if filter_suffixes and not file.suffix.lower() in filter_suffixes:
                    continue
                message.downloadAttachment(file.name, downloadFolder=str(file.parent))
                print(f"📧 '{file.name}' downloaded from '{message.subject}' message of {message.threadId} thread")
        thread.markAsRead()

def login(creds_file: Path, token_file: Path) -> bool:
    """Tries to log into google account to use gmail.

    Returns True if successful, False otherwise.

    Raises a FileNotFoundError if the credentials file is not found."""
    print("📧 Logging in to Gmail...")
    if not creds_file.exists():
        raise FileNotFoundError(f"📧 Credentials file '{creds_file}' not found")
    try:
        init(tokenFile=str(token_file), credentialsFile=str(creds_file))
        print("📧 Login successful")
        return True
    except RefreshError as error:
        token_file.unlink(missing_ok=True)
        return login(creds_file, token_file)
    except Exception as error:
        print(f"📧 Error: {error}")
        return False

def main():
    """Listens for unread emails and downloads attachments."""
    listen_unread_attachments(CREDENTIALS_JSON_FILE_PATH, TOKEN_JSON_FILE_PATH, ATTACHMENTS_DIR)


if __name__ == "__main__":
    main()