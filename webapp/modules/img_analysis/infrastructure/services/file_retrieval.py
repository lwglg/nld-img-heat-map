import os
import requests

from loguru import logger

from webapp.common.constants import INPUT_FOLDER_PATH, GOOGLE_DOCS_URL, FILE_CHUNK_SIZE


def make_requests_to_google_drive(file_id: str, destination: str) -> None:
    """Perform the necessary requests to Google Drive, in order to download the file with given ID."""
    session = requests.Session()

    response = session.get(GOOGLE_DOCS_URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(GOOGLE_DOCS_URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response: requests.Response) -> str | None:
    """Extract confirmation tokem from first request to Google Docs, in order to proceed with download."""

    logger.info("Getting confirmation token from Google Drive...")

    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(
    response: requests.Response, destination: str, chunk_size: int = FILE_CHUNK_SIZE
) -> None:
    """Write download content into a file, by size-limited chunks."""

    logger.info(f"Saving content to '{destination}' with chunk size {chunk_size}...")

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)


async def perform_download(
    files_to_download: list[tuple[str, str]],
    input_folder_path: str = INPUT_FOLDER_PATH,
    file_paths: list[str] = [],
) -> None:
    """Perform file download, given a valid file ID."""

    for file_id, file_ext in files_to_download:
        # Multiplex between folders for JSON (Elasticsearch query dump) and PNG files
        destination_folder = (
            f"{input_folder_path}/elasticsearch"
            if file_ext == "json"
            else f"{input_folder_path}/images"
        )

        os.makedirs(destination_folder, exist_ok=True)

        destination_path = f"{destination_folder}/{file_id}.{file_ext}"

        if os.path.exists(destination_path):
            continue

        logger.warning(f"Downloading '{file_id}' to '{destination_folder}'")

        file_paths.append(destination_path)

        make_requests_to_google_drive(file_id, destination_path)
