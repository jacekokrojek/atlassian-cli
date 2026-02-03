import pytest
from scripts import confluence_utils as cu


def test_extract_page_id_spaces_url():
    src = "https://example.atlassian.net/wiki/spaces/SPACE/pages/12345/Page+Title"
    assert cu.extract_page_id(src) == '12345'


def test_extract_page_id_query_param():
    src = "https://example.atlassian.net/wiki/pages/viewpage.action?pageId=67890"
    assert cu.extract_page_id(src) == '67890'


def test_extract_page_id_none():
    src = "no id here"
    assert cu.extract_page_id(src) is None


def test_extract_space_and_title():
    src = "https://example.atlassian.net/wiki/display/SPACE/Page+Title"
    assert cu.extract_space_and_title(src) == ('SPACE', 'Page Title')
