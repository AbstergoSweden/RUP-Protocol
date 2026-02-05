import os
import pytest
import yaml
import requests
import re
import socket
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PROTOCOL_PATH = ROOT_DIR / "rup-protocol.yaml"


def extract_urls(data):
    urls = []
    if isinstance(data, dict):
        for value in data.values():
            urls.extend(extract_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_urls(item))
    elif isinstance(data, str):
        # Simple regex for http/https URLs
        found = re.findall(r'https?://[^\s<>"|]+|www\.[^\s<>"|]+', data)
        for url in found:
            # Clean up trailing punctuation often found in text
            url = url.rstrip('.,;:)')
            urls.append(url)
    return urls


@pytest.fixture
def protocol_urls():
    with open(PROTOCOL_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return set(extract_urls(data))


def _should_run_link_checks() -> bool:
    return os.getenv("RUP_LINK_CHECKS", "").lower() in {"1", "true", "yes"}


def _fetch_with_retry(url: str, headers: dict[str, str]) -> requests.Response:
    last_error = None
    for attempt in range(3):
        try:
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                response = requests.get(url, headers=headers, timeout=5, stream=True)
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt == 2:
                raise
    raise last_error


def test_no_broken_links(protocol_urls):
    """
    Check all URLs found in the protocol YAML file.
    """
    if not _should_run_link_checks():
        pytest.skip("Set RUP_LINK_CHECKS=1 to enable external link checks")

    # Local dev environments (and some CI sandboxes) may block outbound network/DNS.
    # Skip rather than fail hard when we can't resolve hosts at all.
    try:
        socket.gethostbyname("github.com")
    except OSError:
        pytest.skip("Network/DNS unavailable; skipping external link checks")

    broken_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Skip example/localhost URLs
    skip_domains = ['example.com', 'localhost', '127.0.0.1', 'rup-protocol.dev']

    for url in protocol_urls:
        if any(domain in url for domain in skip_domains):
            continue

        try:
            response = _fetch_with_retry(url, headers)
            if response.status_code >= 400:
                broken_links.append(f"{url} ({response.status_code})")
        except requests.RequestException as e:
            broken_links.append(f"{url} (Error: {str(e)})")

    assert not broken_links, "Found broken links:\n" + "\n".join(broken_links)
