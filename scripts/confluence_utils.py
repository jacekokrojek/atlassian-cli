import re
from urllib.parse import unquote_plus

PAGE_ID_PATTERNS = (
    re.compile(r"/spaces/([^/]+)/pages/(\d+)/[^/]+"),
    re.compile(r"pageId=(\d+)"),
)

PAGE_SPACE_TITLE_PATTERNS = (
    re.compile(r"/display/([^/]+)/([^/]+)"),
)

def extract_page_id(source):
    """Best-effort extraction of a Confluence page id from ``source``."""
    for pattern in PAGE_ID_PATTERNS:
        match = pattern.search(source)
        if match:
            return match.groups()[-1]
    
def extract_space_and_title(source):
    """Best-effort extraction of a Confluence page space and title from ``source``."""
    for pattern in PAGE_SPACE_TITLE_PATTERNS:
        match = pattern.search(source)
        if match:
            groups = match.groups()
            if len(groups) >= 2:
                return groups[0], unquote_plus(groups[1])
